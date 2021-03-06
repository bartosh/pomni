#
# partner.py <Peter.Bienstman@UGent.be>
#

BUFFER_SIZE = 8192


class Partner(object):

    """Common code between Client and Server."""

    def __init__(self, ui):
        self.ui = ui

    def stream_log_entries(self, log_entries, number_of_entries,
                           progress_message):
        # Send log entries across in a streaming manner.
        # Normally, one would use "Transfer-Encoding: chunked" for that, but
        # chunked requests are not supported by the WSGI 1.x standard.
        # However, it seems we can get around sending a Content-Length header
        # if the server knows when the datastream ends. We use the data format
        # footer as a sentinel for that.
        # As the first line in the stream, we send across the number of log
        # entries, so that the other side can track progress.
        # We also buffer the stream until we have sufficient data to send, in
        # order to improve throughput.
        # We also tried compression here, but for typical scenarios that is
        # slightly slower on a WLAN and mobile phone.     
        progress_dialog = self.ui.get_progress_dialog()
        progress_dialog.set_range(0, number_of_entries)
        progress_dialog.set_text(progress_message)
        buffer = self.text_format.log_entries_header(number_of_entries)
        count = 0
        for log_entry in log_entries:
            count += 1
            progress_dialog.set_value(count)
            buffer += self.text_format.repr_log_entry(log_entry)
            if len(buffer) > BUFFER_SIZE:
                yield buffer.encode("utf-8")
                buffer = ""
        buffer += self.text_format.log_entries_footer()
        yield buffer.encode("utf-8")

    def download_log_entries(self, stream, progress_message,
                             callback, context):
        element_loop = self.text_format.parse_log_entries(stream)
        number_of_entries = element_loop.next()
        if number_of_entries == 0:
            return
        progress_dialog = self.ui.get_progress_dialog()
        progress_dialog.set_range(0, number_of_entries)
        progress_dialog.set_text(progress_message)            
        count = 0
        for log_entry in element_loop:
            callback(context, log_entry)
            count += 1
            progress_dialog.set_value(count)
        progress_dialog.set_value(number_of_entries)
        
    def stream_binary_file(self, binary_file, file_size, progress_message):
        progress_dialog = self.ui.get_progress_dialog()
        progress_dialog.set_text(progress_message)
        progress_dialog.set_range(0, file_size)        
        buffer = str(file_size) + "\n" + binary_file.read(BUFFER_SIZE)
        count = BUFFER_SIZE
        while buffer:
            progress_dialog.set_value(count)
            yield buffer
            buffer = binary_file.read(BUFFER_SIZE)
            count += BUFFER_SIZE
        progress_dialog.set_value(file_size)

    def download_binary_file(self, filename, stream, progress_message):
        downloaded_file = file(filename, "wb")            
        file_size = int(stream.readline())
        progress_dialog = self.ui.get_progress_dialog()
        progress_dialog.set_text(progress_message)
        progress_dialog.set_range(0, file_size)
        remaining = file_size
        while remaining:
            if remaining < BUFFER_SIZE:
                downloaded_file.write(stream.read(remaining))
                remaining = 0
            else:
                downloaded_file.write(stream.read(BUFFER_SIZE))
                remaining -= BUFFER_SIZE
            progress_dialog.set_value(file_size - remaining)
        progress_dialog.set_value(file_size)
        downloaded_file.close()
