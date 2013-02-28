import re


HP_OPTIONS = (
    "Healthy",
    "Scratched",
    "Hurt",
    "Wounded",
    "Battered",
    "Beaten",
    "Critical",
    "Incapacitated"
)

MV_OPTIONS = (
    "Fresh",
    "Tiring",
    "Winded",
    "Haggard"
)

SP_OPTIONS = (
    "Bursting",
    "Trickling"
)


PROMPT_RE = re.compile(r"""(?P<light>[*o])
                           \s
                           (?:
                            (?P<position>[RS])
                           \s)?
                           HP:(?P<hp>{HP_OPTIONS})
                           \s
                           (?:
                            (?P<sptype>[SD]P):
                            (?P<sp>{SP_OPTIONS})
                           \s)?
                           MV:(?P<mv>{MV_OPTIONS})
                           \s
                           (?:
                            -\s
                            (?P<e1name>[^:]+):
                            \s
                            (?P<e1hp>{HP_OPTIONS})
                           \s)?
                           (?:
                            -\s
                            (?P<e2name>[^:]+):
                            \s
                            (?P<e2hp>{HP_OPTIONS})
                           \s)?
                           >
                       """.format(HP_OPTIONS="|".join(HP_OPTIONS),
                                  SP_OPTIONS="|".join(SP_OPTIONS),
                                  MV_OPTIONS="|".join(MV_OPTIONS)), re.X)


COMM_RE = re.compile(r"""^(?P<who>.*)\s
                          (?P<how>chats|narrates|yells|says|shouts)\s
                          '.*'$""", re.X)


def parse_log(log):
    """Takes a log and parses it, returning the input as a list of pairs
    (line, info)"""

    for i, line in enumerate(log.splitlines()):
        # Strip the line to remove leading/trailing spaces
        # We keep the original line reference so we can return it later
        orig = line
        line = line.strip()

        # Clear our hints on each line
        hints = []

        # If the line has no content, then yield early
        if not line:
            yield (i, orig, [])
            continue

        # Otherwise, see if it's a prompt
        m = PROMPT_RE.search(line)
        if m:
            # If it is a prompt, see if we can get a hint
            # Trolls cannot ride
            # Channelers have SP
            # Fades have DP
            groups = m.groupdict()
            if groups.get('sptype') == 'SP':
                hints.append('Class: Channeler')
            elif groups.get('sptype') == 'DP':
                hints.append('Class: Fade')

            if groups.get('position') == 'R':
                hints.append('Faction: LS')
                hints.append('Faction: SS')

            if groups.get('e1name'):
                hints.append('Cast: ' + groups.get('e1name'))

            if groups.get('e2name'):
                hints.append('Cast: ' + groups.get('e2name'))

            # Now, remove the prompt from the line for further processing
            line = PROMPT_RE.sub('', line).strip()

        # If the line is a comm, then we can get the Extras hint and purge it
        m = COMM_RE.search(line)
        if m:
            groups = m.groupdict()
            hints.append('Extras: ' + groups.get('who'))

            line = COMM_RE.sub('', line).strip()

        yield (i, orig, hints)


if __name__ == "__main__":
    import pprint

    text = [
        "* R HP:Wounded MV:Fresh > l",
        "* R HP:Wounded SP:Bursting MV:Fresh > l",
        "* R HP:Wounded DP:Trickling MV:Fresh > l",
        "* R HP:Wounded MV:Fresh - Haznak: Hurt > ",
        "* HP:Wounded MV:Fresh - Haznak: Hurt > ",
        "o HP:Wounded MV:Fresh - Haznak: Hurt > ",
        "* R HP:Battered MV:Fresh - Saif: Battered - a ramshorned trolloc: Wounded > ",  # noqa
        "Haznak narrates 'adsfasdfqwe'",
        "Mythras says 'say hello to your mother, trebek.'",
    ]
    text = "\r\n".join(text)

    """
    import os
    testdata = os.path.join(os.path.dirname(__file__), 'testdata')
    text = open(testdata + '/log1.txt').read()
    """

    pprint.pprint(list(parse_log(text)))
