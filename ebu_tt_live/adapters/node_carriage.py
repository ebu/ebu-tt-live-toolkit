
from ebu_tt_live.node.base import INode
from ebu_tt_live.carriage.base import IProducerCarriage, IConsumerCarriage


class NodeCarriageAdapter(INode, IProducerCarriage, IConsumerCarriage):
    pass