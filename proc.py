# Simple wrapper around subprocess
from subprocess import check_call

def run( *args, **kw ):
    "Wrapper around check_call that sets shell to True"
    kw["shell"] = True

    return check_call( *args, **kw )

