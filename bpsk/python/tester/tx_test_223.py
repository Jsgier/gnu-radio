import time
import zmq
import pmt

TX_ENDPOINT = "tcp://127.0.0.1:5555"  # gateway PUSH -> GNU Radio zmq_msg_source (PULL)

def make_pdu(payload: bytes):
    meta = pmt.PMT_NIL
    vec = pmt.init_u8vector(len(payload), list(payload))
    return pmt.cons(meta, vec)

def main():
    ctx = zmq.Context.instance()
    sock = ctx.socket(zmq.PUSH)
    sock.connect(TX_ENDPOINT)

    counter = 0
    while True:
        # Make exactly 223 bytes
        payload = bytes([(counter + i) & 0xFF for i in range(223)])
        pdu = make_pdu(payload)
        wire = pmt.serialize_str(pdu)

        sock.send(wire)
        print(f"Sent PDU #{counter} (len={len(payload)})")
        counter += 1
        time.sleep(0.1)

if __name__ == "__main__":
    main()
