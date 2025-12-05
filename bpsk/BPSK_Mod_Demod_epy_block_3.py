import pmt
from gnuradio import gr
import sys

class TestPatternChecker_PDU(gr.basic_block):
    """
    Checks received PDUs against the known test pattern:

    Input PDU payload format:
        [seq_hi][seq_lo][pattern bytes...]

    - seq = 16-bit sequence number
    - pattern[i] = (i + seq) & 0xFF for i >= 2

    It:
      * Recomputes expected payload for that seq
      * Compares byte-by-byte
      * Tracks total frames, bad frames, and total byte errors
      * Prints stats to stdout if verbose=True
    """

    def __init__(self, expected_len=200, verbose=True):
        gr.basic_block.__init__(self,
            name="TestPatternChecker_PDU",
            in_sig=None,
            out_sig=None)

        self.expected_len = int(expected_len)
        self.verbose = bool(verbose)

        self.total_frames = 0
        self.bad_frames = 0
        self.total_byte_errors = 0

        # one input PDU port called "in"
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_pdu)

    def _expected_payload(self, seq):
        """
        Reconstruct the expected payload for a given sequence number.
        Must match whatever TestPatternSource_PDU generates.
        """
        payload = bytearray(self.expected_len)
        payload[0] = (seq >> 8) & 0xFF
        payload[1] = seq & 0xFF
        for i in range(2, self.expected_len):
            payload[i] = (i + seq) & 0xFF
        return payload

    def handle_pdu(self, pdu):
        meta = pmt.car(pdu)
        data = bytearray(pmt.u8vector_elements(pmt.cdr(pdu)))

        if len(data) < 2:
            # too short to contain seq
            return

        # If RS or padding changed the length, you can either:
        #  - enforce exact length
        #  - or compare up to min(len(data), expected_len)
        if len(data) != self.expected_len:
            if self.verbose:
                sys.stdout.write(
                    "Checker: length mismatch (rx=%d, expected=%d)\n"
                    % (len(data), self.expected_len)
                )
                sys.stdout.flush()
            # use the common subset for comparison
            compare_len = min(len(data), self.expected_len)
            data = data[:compare_len]
        else:
            compare_len = len(data)

        seq = (data[0] << 8) | data[1]
        expected = self._expected_payload(seq)[:compare_len]

        self.total_frames += 1

        byte_errors = 0
        for i in range(compare_len):
            if data[i] != expected[i]:
                byte_errors += 1

        if byte_errors > 0:
            self.bad_frames += 1
            self.total_byte_errors += byte_errors

        if self.verbose:
            sys.stdout.write(
                "Frame %d (seq=%d): len=%d, byte_errors=%d, "
                "bad_frames=%d/%d, total_byte_errors=%d\n"
                % (self.total_frames, seq, compare_len,
                   byte_errors, self.bad_frames,
                   self.total_frames, self.total_byte_errors)
            )
            sys.stdout.flush()
