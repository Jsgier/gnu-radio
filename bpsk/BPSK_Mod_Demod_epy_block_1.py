import numpy
import pmt
from gnuradio import gr

class blk(gr.sync_block):
    """
    Stream block that watches for 'CCSDS_frame' tags and, at the same
    offset, injects a 'frame_len' tag with value 259.

    Assumes:
      - Input and output are uint8 (bytes).
      - Stream is 1:1 passthrough.
    """

    def __init__(self, frame_len=2072):
        gr.sync_block.__init__(
            self,
            name="frame_len_from_ccsds_tag",
            in_sig=[numpy.uint8],
            out_sig=[numpy.uint8],
        )

        # Keys we'll use
        self.key_ccsds_frame = pmt.intern("CCSDS_frame")
        self.key_frame_len   = pmt.intern("frame_len")
        self.frame_len = pmt.from_long(frame_len)

    def work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        # Passthrough
        out[:] = inp

        nread    = self.nitems_read(0)
        nwritten = self.nitems_written(0)
        nitems   = len(inp)

        # Get all tags in this window of input
        tags = self.get_tags_in_window(0, 0, nitems)

        for t in tags:
            # Only react to CCSDS_frame tags
            if t.key == self.key_ccsds_frame:
                # Convert absolute tag offset to relative index within this work() call
                rel_index = t.offset - nread

                if 0 <= rel_index < nitems:
                    # Compute absolute output offset for this work() chunk
                    out_offset = nwritten + rel_index

                    # Inject frame_len tag at the same logical position
                    self.add_item_tag(
                        0,                          # output port
                        out_offset,                 # absolute offset on output
                        self.key_frame_len,         # key: "frame_len"
                        self.frame_len,       # value: 259
                        t.srcid                     # preserve original srcid
                    )

        return nitems
