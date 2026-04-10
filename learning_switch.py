from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# MAC table: {dpid: {mac: port}}
mac_to_port = {}


def _handle_ConnectionUp(event):
    log.info("Switch connected: %s", event.connection)


def _handle_PacketIn(event):
    packet = event.parsed

    # Ignore incomplete packets
    if packet is None:
        return

    dpid = event.connection.dpid
    src = packet.src
    dst = packet.dst
    in_port = event.port

    # Initialize table for this switch
    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    # ==============================
    # [F1] MAC LEARNING
    # ==============================
    mac_to_port[dpid][src] = in_port
    log.info("Learned MAC: %s on port %s", src, in_port)

    # ==============================
    # [F3] FORWARDING
    # ==============================
    if dst in mac_to_port[dpid]:
        # Destination known → forward
        out_port = mac_to_port[dpid][dst]

        log.info("Forwarding %s -> %s via port %s", src, dst, out_port)

        # ==============================
        # [F2] INSTALL FLOW RULE
        # ==============================
        msg = of.ofp_flow_mod()
        msg.match.dl_src = src
        msg.match.dl_dst = dst
        msg.idle_timeout = 10
        msg.hard_timeout = 30
        msg.actions.append(of.ofp_action_output(port=out_port))

        event.connection.send(msg)

        # Send current packet
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.in_port = in_port
        event.connection.send(msg)

    else:
        # Destination unknown → FLOOD (IMPORTANT)
        log.info("Flooding packet")

        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        msg.in_port = in_port
        event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Learning Switch Started 🚀")