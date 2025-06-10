import ADSModule

def servers():
    # return a list of dicts with your "servers" (in this case just one bot)
    return [{
        'name': 'Discord Music Bot',
        'startfile': 'bot.py',
        'type': 'python'
    }]

ADSModule.register_module(servers=servers)

