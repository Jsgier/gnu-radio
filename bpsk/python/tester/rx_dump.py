import zmq
import pmt

RX_ENDPOINT = "tcp://127.0.0.1:5556"

def pdu_to_bytes(pdu):
    meta = pmt.car(pdu)
    vec  = pmt.cdr(pdu)
    b = bytes(pmt.u8vector_elements(vec))
    return meta, b

def main():
    ctx = zmq.Context.instance()
    sock = ctx.socket(zmq.PULL)
    sock.connect(RX_ENDPOINT)

    poller = zmq.Poller()
    poller.register(sock, zmq.POLLIN)

    print("Listening (Ctrl+C to quit)...")
    try:
        while True:
            events = dict(poller.poll(timeout=250))  # ms
            if sock in events:
                wire = sock.recv()
                pdu = pmt.deserialize_str(wire)
                meta, payload = pdu_to_bytes(pdu)
                print(f"Got PDU len={len(payload)} first16={payload[:16].hex(' ')}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        sock.close(0)
        ctx.term()

if __name__ == "__main__":
    main()
