import importlib


def process_event(event, package, module):
    # print(f"Importing {package}.{module}")
    mod = importlib.import_module(package)
    lcm_t = eval(f'mod.{module}')
    msg = lcm_t.decode(event.data)

    return msg


def event_headers(event, package, module):
    # decode the data if its the channel we want
    msg = process_event(event, package, module)

    # ignore the methods in this list
    fields = [field for field in dir(msg) if not field.startswith('_')]

    cols = list()

    # lcm event info
    cols.append("evt_channel")
    cols.append("evt_number")
    cols.append("evt_timestamp")
    for field in fields:
        value = getattr(msg, field)

        if callable(value):
            continue
        # print(field+str(type(field)))

        if type(value) is str:
            cols.append(str(value))
            continue

        try:
            iterator = iter(value)
        except TypeError:
            # not a list
            cols.append(str(field))
            # print(str(field))
        else:
            # its a list
            i = 0
            for idx, val in enumerate(value):
                s = str(field).replace(',', '_')
                try:
                    s += "_%s" % val.name
                except:
                    s += "_%i" % i
                    i += 1
                # print(s)
                cols.append(str(s))

    return cols


def event_data(event, package, module):
    def append_data(dat, amt):
        try:
            if type(amt) is str or type(amt) is str:
                s = str(amt).replace(',', '_')
                dat.append(str(s))
                return

            else:
                dat.append(amt)
                return

        except TypeError:
            pass

        except AttributeError as ae:
            pass

    data = list()

    msg = process_event(event, package, module)

    # ignore the methods in this list
    fields = [field for field in dir(msg) if not field.startswith('_')]

    # lcm event info
    data.append("%s" % event.channel)
    data.append(event.eventnum)
    data.append(event.timestamp)

    for field in fields:
        value = getattr(msg, field)

        if callable(value):
            continue

        if type(value) is str:
            data.append(str(value))
            continue

        try:
            iterator = iter(value)
        except TypeError:
            # not a list
            append_data(data, value)
        else:
            # its a list
            for val in value:
                append_data(data, val)

    return data
