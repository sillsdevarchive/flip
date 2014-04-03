#!/bin/sed -rf

# Only on lines with an \s marker subititue all \pn markers for \z_spn and all
# \z_pg markers for \z_spg.  This assumes that the \s marker is a single line
# and we are applying the expression to the entire line.
/\\s[[:digit:]]?\s/ {
  s/\\pn(\*?)/\\z_spn\1/g
  s/\\z_pg(\*?)/\\z_spg\1/g
}

# Inside a \f marker, which could be anywhere on any line, replace \pn with
# \z_fnpn & \z_pg with \z_fnpg.  This could break if there was a \f in a \s
# line.
/\\f\s.*\\f\*/ {
  : loop1
  s/(\\f\s.*)\\pn(\*?)(.*\\f\*)/\1\\z_fnpn\2\3/g
  s/(\\f\s.*)\\z_pg(\*?)(.*\\f\*)/\1\\z_fnpg\2\3/g
  t loop1
}

# Look again in the \f for any \fk markers and now change any \z_fnpn with
# \z_fnkpn.
/\\f\s.*\\fk\s.*\\f\*/ {
  : loop2
  s/(\\f\s.*\\fk\s[^\\]*)\\z_fnpn(\s[^\\]*)\\z_fnpn\*(.*\\f\*)/\1\\z_fnkpn\2\\z_fnkpn*\3/g
  t loop2
}

# Look again in the \f for any \fk markers and now change any \z_fnpg with \z_fnkpg.
/\\f\s.*\\fk\s.*\\f\*/ {
  : loop3
  s/(\\f\s.*\\fk\s[^\\]*)\\z_fnpg(\s[^\\]*)\\z_fnpg\*(.*\\f\*)/\1\\z_fnkpg\2\\z_fnkpg*\3/g
  t loop3
}

# Loop again in the \f for any \fq markers and now change any \z_fnpn with
# \z_fnqpn.
/\\f\s.*\\fq\s.*\\f\*/ {
  : loop4
  s/(\\f\s.*\\fq\s[^\\]*)\\z_fnpn(\s[^\\]*)\\z_fnpn\*(.*\\f\*)/\1\\z_fnqpn\2\\z_fnqpn*\3/g
  t loop4
}

# Loop again in the \f for any \fq markers and now change any \z_fnpg with
# \z_fnqpg.
/\\f\s.*\\fq\s.*\\f\*/ {
  : loop5
  s/(\\f\s.*\\fq\s[^\\]*)\\z_fnpg(\s[^\\]*)\\z_fnpg\*(.*\\f\*)/\1\\z_fnqpg\2\\z_fnqpg*\3/g
  t loop5
}
