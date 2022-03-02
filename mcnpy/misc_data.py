from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Debug(DebugBase):

    PROPERTIES = ['x1',
        'x2',
        'x3',
        'x4',
        'x5',
        'x6',
        'x7',
        'x8',
        'x9',
        'x10',
        'x11',
        'x12',
        'x13',
        'x14',
        'x15',
        'x16',
        'x17',
        'x18',
        'x19',
        'x23',
        'x24',
        'x27',
        'x28',
        'x32',
        'x33',
        'x34',
        'x35',
        'x36',
        'x37',
        'x38',
        'x39',
        'x40',
        'x41',
        'x42',
        'x43',
        'x44',
        'x45',
        'x46',
        'x47',
        'x48',
        'x49',
        'x50',
        'x51',
        'x52',
        'x53',
        'x54',
        'x55',
        'x60',
        'x61',
        'x62',
        'x64',
        'x65',
        'x66',
        'x67',
        'x69',
        'x70',
        'x71',
        'x72',
        'x75',
        'x76',
        'x77',
        'x78',
        'x79',
        'x81',
        'x82',
        'x83',
        'x84',
        'x85',
        'x86',
        'x87',
        'x88',
        'x89',
        'x90',
        'x91',
        'x92',
        'x100',]

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])
        

    """# Applies defaults to avoid serializing nulls.
    # Automatically called when adding card to deck.
    def _defaults(self):
        entry = len(self.PROPERTIES)-1
        for k in self.PROPERTIES:
            if getattr(self, k) is None:
                setattr(self, k, 'J')
            else:
                entry = self.PROPERTIES.index(k)
        # Avoid printing all options if possible
        if entry != len(self.PROPERTIES)-1:
            for k in self.PROPERTIES[entry+1:]:
                setattr(self, k, None)"""

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override