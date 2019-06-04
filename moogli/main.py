from moogli.core import _moogli

DISTAL          = 0
AVERAGED        = 1
PROXIMAL_DISTAL = 2


def read_morphology_from_moose(name = "", path = "", radius = DISTAL):
    import moose
    morphology = _moogli.Morphology(name, 1)
    compartments = moose.wildcardFind(path + "/##[ISA=CompartmentBase]")
    for compartment in compartments:
        distal_diameter = compartment.diameter
        try:
            parent_compartment = compartment.neighbors["raxial"][0]
            proximal_diameter  = parent_compartment.diameter
        except IndexError:
            proximal_diameter = distal_diameter

        if   radius == DISTAL          :
            proximal_diameter = distal_diameter
        elif radius == AVERAGED        :
            distal_diameter = proximal_diameter =  ( distal_diameter
                                                   + proximal_diameter
                                                   ) / 2.0

        morphology.add_compartment(     compartment.path
                , compartment.parent.path
                , compartment.x0          * 10000000
                , compartment.y0          * 10000000
                , compartment.z0          * 10000000
                , proximal_diameter       * 10000000
                , compartment.x           * 10000000
                , compartment.y           * 10000000
                , compartment.z           * 10000000
                , distal_diameter         * 10000000
                )
    return morphology
