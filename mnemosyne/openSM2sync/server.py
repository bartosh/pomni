#
# server.py - Max Usachev <maxusachev@gmail.com>
#             Ed Bartosh <bartosh@gmail.com>
#             Peter Bienstman <Peter.Bienstman@UGent.be>

import os
import cgi
import base64
import select
import tarfile
import cStringIO
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

from utils import tar_file_size
from data_format import DataFormat


class Server(WSGIServer):

    """Note that the current implementation of the server can only handle one
    sync request at the time. it is *NOT* yet suited to deploy in a multiuser
    context over the internet, as simultaneous requests from different users
    could get mixed up.

    """
    
    program_name = "unknown-SRS-app"
    program_version = "unknown"
    capabilities = None  # TODO: list possibilies.

    stop_after_sync = False # Setting this True is useful for the testsuite. 

    def __init__(self, host, port, ui):
        WSGIServer.__init__(self, (host, port), WSGIRequestHandler)
        self.set_app(self.wsgi_app)
        self.ui = ui
        self.data_format = DataFormat()
        self.stopped = False
        self.logged_in = False
        self.id = "TODO"
        self.client_info = {}
        self.number_of_client_log_entries_to_sync = None

    def wsgi_app(self, environ, start_response):
        status, mime, method, args = self.get_method(environ)
        response_headers = [("Content-type", mime)]
        start_response(status, response_headers)
        if method:
            return getattr(self, method)(environ, **args)
        else:
            return status

    def serve_forever(self):
        self.ui.status_bar_message("Waiting for client connection...")
        timeout = 1
        while not self.stopped:
            if select.select([self.socket], [], [], timeout)[0]:
                self.handle_request()
        self.socket.close()

    def stop(self):
        self.stopped = True

    def get_method(self, environ):

        """Checks for method existence in service and checks for right request
        params.

        """

        def compare_args(list1, list2):
            
            """Compares two lists or tuples."""
            
            for item in list1:
                if not item in list2:
                    return False
            return True

        if environ.has_key("HTTP_AUTHORIZATION"):
            login, password = base64.decodestring(\
                environ["HTTP_AUTHORIZATION"].split(" ")[-1]).split(":")
            if self.authorise(login, password):
                self.logged_in = True
                status = "200 OK"
            else:
                self.logged_in = False
                status = "403 Forbidden"
            return status, "text/plain", None, None
        else:
            if not self.logged_in:
                return "403 Forbidden", "text/plain", None, None
            method = (environ["REQUEST_METHOD"] + \
                "_".join(environ["PATH_INFO"].split("/"))).lower()
            if hasattr(self, method) and callable(getattr(self, method)):
                args = cgi.parse_qs(environ["QUERY_STRING"])
                args = dict([(key, val[0]) for key, val in args.iteritems()])
                if getattr(self, method).func_code.co_argcount-2 == len(args) \
                    and compare_args(args.keys(), getattr(self, method). \
                        func_code.co_varnames):                
                    return "200 OK", "xml/text", method, args
                else:
                    return "400 Bad Request", "text/plain", None, None
            else:
                return "404 Not Found", "text/plain", None, None

    # The following functions are to be overridden by the actual server code,
    # to implement e.g. authorisation and storage.

    def authorise(self, login, password):

        """Returns true if password correct for login."""

        raise NotImplementedError

    def open_database(self, database_name):

        """Sets self.database to a database object for the database named
        'database_name'.

        """

        raise NotImplementedError

    # The following are methods that are supported by the server through GET
    # and PUT calls. 'get_foo_bar' gets executed after a 'GET /foo/bar'
    # request. Similarly, 'put_foo_bar' gets executed after a 'PUT /foo/bar'
    # request.

    def get_server_info(self, environ):
        self.ui.status_bar_message("Sending server info to the client...")
        server_info = {"id": self.id, "program_name": self.program_name,
            "program_version": self.program_version,
            "capabilities": self.capabilities}
        return self.data_format.repr_partner_info(server_info)

    def put_client_info(self, environ):
        self.ui.status_bar_message("Receiving client info...")
        try:
            client_info_repr = environ["wsgi.input"].readline()
        except:
            return "CANCEL"
        self.client_info = \
            self.data_format.parse_partner_info(client_info_repr)
        self.open_database(self.client_info["database_name"])
        self.database.backup()
        self.database.create_partnership_if_needed_for(self.client_info["id"])
        return "OK"
        
    def put_number_of_client_log_entries_to_sync(self, environ):
        try:
            socket = environ["wsgi.input"]
            self.number_of_client_log_entries_to_sync = int(socket.readline())
        except:
            return "CANCEL"
        else:
            return "OK"
    
    def get_number_of_server_log_entries_to_sync(self, environ):
        return str(self.database.number_of_log_entries_to_sync_for(\
            self.client_info["id"]))

    def get_server_log_entries(self, environ):
        self.ui.status_bar_message("Sending log entries to client...")
        log_entries = self.database.number_of_log_entries_to_sync_for(\
            self.client_info["id"])
        progress_dialog = self.ui.get_progress_dialog()
        progress_dialog.set_range(0, log_entries)
        progress_dialog.set_text("Sending log entries to client...")
        chunk = "<openSM2sync>"
        count = 0
        for log_entry in self.database.log_entries_to_sync_for(\
            self.client_info["id"]):
            count += 1
            progress_dialog.set_value(count)
            chunk += self.data_format.repr_log_entry(log_entry).\
                encode("utf-8")
            if len(chunk) > 8192:
                yield chunk
                chunk = ""
        chunk += "</openSM2sync>"
        yield chunk
        
    def put_client_log_entries(self, environ):
        self.ui.status_bar_message("Receiving client log entries...")
        progress_dialog = self.ui.get_progress_dialog()
        progress_dialog.set_range(0, self.number_of_client_log_entries_to_sync)
        progress_dialog.set_text("Receiving client log entries...")
        # Since chunked requests are not supported by the WSGI 1.x standard,
        # the client does not set Content-Length in order to be able to
        # stream the log entries. Therefore, it is our responsability that we
        # consume the entire stream, nothing more and nothing less. For that,
        # we use the closing openSM2sync tag followed by \n as a sentinel.
        # For simplicity, we also keep the entire stream in memory, as the
        # server is not expected to be resource limited.
        socket = environ["wsgi.input"]        
        lines = []
        line = socket.readline()
        lines.append(line)
        while not line.endswith("</openSM2sync>\n"):
            line = socket.readline()
            lines.append(line)
        # In order to do conflict resolution easily, one of the sync partners
        # has to have both logs in memory. We do this at the server side, as
        # the client could be resource-limited mobile device.
        self.client_log = []
        count = 0
        data_stream = cStringIO.StringIO("".join(lines))
        for log_entry in self.data_format.parse_log_entries(data_stream):
            self.client_log.append(log_entry)
            count += 1
            progress_dialog.set_value(count)
        self.ui.status_bar_message("Waiting for client to finish...")
        return "OK"

    def put_client_media_files_size(self, environ):
        try:
            socket = environ["wsgi.input"]
            self.client_media_files_size = int(socket.readline())
        except:
            return "CANCEL"
        else:
            return "OK"
        
    def put_client_media_files(self, environ):
        self.ui.status_bar_message("Receiving client media files...")
        try:
            socket = environ["wsgi.input"]           
            tar_pipe = tarfile.open(mode="r|", fileobj=socket)
            # Work around http://bugs.python.org/issue7693.
            tar_pipe.extractall(self.database.mediadir().encode("utf-8"))
        except:
            return "CANCEL"
        return "OK"

    def get_server_media_files_size(self, environ):
        filenames = list(self.database.media_filenames_to_sync_for(\
            self.client_info["id"]))
        size = tar_file_size(self.database.mediadir(), filenames)
        return str(size)
    
    def get_server_media_files(self, environ):
        self.ui.status_bar_message("Sending media files to client...")
        self.database.check_for_updated_media_files()
        filenames = self.database.media_filenames_to_sync_for(\
            self.client_info["id"])
        if len(filenames) == 0:
            yield "OK"
            return
        try:
            BUFFER_SIZE = 8192
            import tempfile
            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            tmp_file_name = tmp_file.name
            saved_path = os.getcwdu()
            os.chdir(self.database.mediadir())
            tar_pipe = tarfile.open(mode="w|", fileobj=tmp_file,
                bufsize=BUFFER_SIZE, format=tarfile.PAX_FORMAT)
            for filename in self.database.media_filenames_to_sync_for(\
                self.client_info["id"]):
                tar_pipe.add(filename)
            tar_pipe.close()
            tmp_file = file(tmp_file_name, "rb")
            file_size = os.path.getsize(tmp_file_name)
            progress_dialog = self.ui.get_progress_dialog()
            progress_dialog.set_range(0, file_size)
            progress_dialog.set_text("Sending media files to client...")
            chunk = tmp_file.read(BUFFER_SIZE)
            count = BUFFER_SIZE
            while chunk:
                progress_dialog.set_value(count)
                yield chunk
                chunk = tmp_file.read(BUFFER_SIZE)
                count += BUFFER_SIZE
            progress_dialog.set_value(file_size)
            os.remove(tmp_file_name)
            os.chdir(saved_path)
        except:
            yield "CANCEL"

    def get_sync_finish(self, environ):
        self.ui.status_bar_message("Waiting for client to finish...")
        for log_entry in self.client_log:
            self.database.apply_log_entry(log_entry)
        self.database.update_last_sync_log_entry_for(self.client_info["id"])
        self.logged_in = False
        if self.stop_after_sync:
            self.stop()
        return "OK"
