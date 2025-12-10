import pmt
from gnuradio import gr
import time
import threading

class TestPatternSource_PDU(gr.basic_block):
    """
    Periodically emits PDUs with a simple test pattern:
    [seq_hi][seq_lo][payload bytes...]

    - seq: 16-bit counter
    - payload filled with pattern (e.g. incrementing or 0xAA/0x55)
    """

    def __init__(self, payload_len=200, interval_ms=100):
        gr.basic_block.__init__(self,
            name="TestPatternSource_PDU",
            in_sig=None,
            out_sig=None)

        self.payload_len = int(payload_len)
        self.interval = float(interval_ms) / 1000.0
        self.seq = 0

        self.message_port_register_out(pmt.intern('out'))

        # start worker thread
        self._stop = False
        self.thread = threading.Thread(target=self._worker)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self._stop = True
        try:
            self.thread.join(timeout=0.1)
        except:
            pass
        return super().stop()

    def _make_payload(self):
        # 2-byte sequence number + payload_len-2 bytes of pattern
        payload = bytearray(self.payload_len)
        seq = self.seq & 0xFFFF
        payload[0] = (seq >> 8) & 0xFF
        payload[1] = seq & 0xFF

        # simple pattern: incrementing bytes
        ## simpler pattern enabled: same byte every time. 
        for i in range(1, self.payload_len):
            payload[i] = (i + seq) & 0xFF
            #payload[i] = (i) & 0xFF

        #self.seq = (self.seq + 1) & 0xFFFF
        self.seq = (self.seq) & 0xFFFF
        return payload

    def _worker(self):
        while not self._stop:
            payload = self._make_payload()
            meta = pmt.make_dict()  # empty metadata

            vec = pmt.init_u8vector(len(payload), payload)
            pdu = pmt.cons(meta, vec)

            self.message_port_pub(pmt.intern('out'), pdu)
            time.sleep(self.interval)
