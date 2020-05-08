def classFactory(iface):
    from .gardener import Gardener
    return Gardener(iface)