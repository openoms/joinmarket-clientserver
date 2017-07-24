# joinmarket-clientserver

Joinmarket refactored to separate client and backend operations

**NOTE: To use current Joinmarket, use the [latest release](https://github.com/AdamISZ/joinmarket-clientserver/releases).
The master branch is upgraded for segwit and to be used only for testing until the next release.**

### Quickstart

You need to follow the [install guide](docs/INSTALL.md).

The above document will point you to the [segwit upgrade guide](docs/SEGWIT-UPGRADE.md) if you need to update your wallet.

If you are new, follow and read the links in the [usage guide](docs/USAGE.md).

If you are not new to Joinmarket, the notes in the [scripts readme](scripts/README.md) help to understand what has and hasn't changed about the scripts.

There is a joinmarket-qt GUI included but it's not yet ready for the new segwit version.

### Notes on architectural changes (can be ignored)

Motivation: By separating the code which manages conversation with other
Joinmarket participants from the code which manages this participant's Bitcoin
wallet actions, we get a considerable gain at a minor cost of an additional layer:
code dependencies for each part are much reduced, security requirements of the 
server/daemon layer are massively reduced (which can have several advantages such as
it being more acceptable to distribute this layer as a binary), and client code
can be written, implementing application-level logic (do join with coins X under condition X)
using other Bitcoin libraries, or wallets, without knowing anything about
Joinmarket's inter-participant protocol. An example is my work on the Joinmarket
electrum [plugin](https://github.com/AdamISZ/electrum-joinmarket-plugin).

It also
means that updates to the Bitcoin element of Joinmarket, such as P2SH and segwit, should
have extremely minimal to no impact on the backend code, since the latter just implements
communication of a set of formatted messages, and allows the client to decide on
their validity beyond simply syntax.

Joinmarket's own [messaging protocol](https://github.com/JoinMarket-Org/JoinMarket-Docs/blob/master/Joinmarket-messaging-protocol.md) is thus enforced *only* in the server/daemon.

The client and server currently communicate using twisted.protocol.amp, see
[AMP](https://amp-protocol.net/),
and the specification of the communication between the client and server is isolated to
[this](https://github.com/AdamISZ/joinmarket-clientserver/blob/master/jmbase/jmbase/commands.py) module.
Currently the messaging layer of Joinmarket is IRC-only (but easily extensible, see [here](https://github.com/JoinMarket-Org/joinmarket/issues/650).
The IRC layer is also implemented here using Twisted, reducing the complexity required with threading.

The "server" is just a daemon service that can be run as a separate process (see `scripts/joinmarketd.py`), or for convenience in the same process (the default for command line scripts).

### TESTING

Instructions for developers for testing [here](docs/TESTING.md).
