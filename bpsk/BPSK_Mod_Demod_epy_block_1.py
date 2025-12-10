import numpy
import pmt
from gnuradio import gr

class blk(gr.sync_block):
    """
    Stream block that watches for 'CCSDS_frame' tags and injects a
    'frame_len' tag with value frame_len at the **same** offset.

    Assumes:
      - Input and output are uint8 bits (0/1), 1 bit per item.
      - frame_len is in items (bits).
    """

    def __init__(self, frame_len=2072, verbose=False):
        gr.sync_block.__init__(
            self,
            name="frame_len_from_ccsds_tag",
            in_sig=[numpy.uint8],
            out_sig=[numpy.uint8],
        )

        self.key_ccsds_frame = pmt.intern("CCSDS_frame")
        self.key_frame_len   = pmt.intern("frame_len")

        self.frame_len       = int(frame_len)
        self.frame_len_value = pmt.from_long(self.frame_len)

        self.verbose = bool(verbose)

    def work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        # Pass-through
        out[:] = inp

        nread    = self.nitems_read(0)
        nwritten = self.nitems_written(0)
        nitems   = len(inp)

        # Get tags in this input window
        tags = self.get_tags_in_window(0, 0, nitems)

        for t in tags:
            if t.key == self.key_ccsds_frame:
                # Absolute offset where CCSDS_frame tag occurred
                abs_in_offset = t.offset

                # Relative index within this work() buffer
                rel_index = abs_in_offset - nread

                if 0 <= rel_index < nitems:
                    abs_out_offset = nwritten + rel_index

                    # Add frame_len tag at the **same** logical offset
                    self.add_item_tag(
                        0,
                        abs_out_offset,
                        self.key_frame_len,
                        self.frame_len_value,
                        t.srcid
                    )

                    if self.verbose:
                        print(
                            "[frame_len_from_ccsds_tag] CCSDS_frame at {}, "
                            "frame_len tag at {}, len={}".format(
                                int(abs_in_offset), int(abs_out_offset), self.frame_len
                            )
                        )

        return nitems
