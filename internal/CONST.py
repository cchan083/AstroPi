class Constants:
    def __init__(self, **kwargs):
        for arg, value in kwargs.items():
            if not isinstance(value, Value):
                raise TypeError(f"Expected an instance of Value, got {type(value)}")
            setattr(self, arg, value.value)

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"Cannot modify constant {name}")
        super().__setattr__(name, value)

###########################################XC

class Value:
    def __init__(self, val):
        self.value = val

class I32(Value):
    def __init__(self, val):
        super().__init__(val)

class String(Value):
    def __init__(self, val):
        super().__init__(val)


###########################################

CONST = Constants(
    # SPEED CALCULATION CONSTANTS
    gsd                 =       I32( 12648 ),
    feature_num         =       I32( 2000  ),
    data_log_interval   =       I32( 10    ), # SECONDS
    data_log_duration   =       I32( 1     ), # MINS
)

##########################################