import numpy as np

x = np.linspace(1, 0, 101)
y = np.linspace(0, 1, 101)
z = np.linspace(0, -0.1, 2)

with open('block.p3d', 'w') as plot3d:
    plot3d.write('1\n')
    plot3d.write('{:<4d} {:<4d} {:<4d}\n'.format(len(x), len(y), len(z)))
    for k in range(0, len(z)):
        for j in range(0, len(y)):
            for i in range(0, len(x)):
                plot3d.write('{:<4.4f} '.format(x[i]))
    plot3d.write('\n')
    for k in range(0, len(z)):
        for j in range(0, len(y)):
            for i in range(0, len(x)):
                plot3d.write('{:<4.4f} '.format(y[j]))
    plot3d.write('\n')
    for k in range(0, len(z)):
        for j in range(0, len(y)):
            for i in range(0, len(x)):
                plot3d.write('{:<4.4f} '.format(z[k]))

nmf_content = """# ===== Neutral Map File ===========================================================
# ==================================================================================
# Block#   IDIM   JDIM   KDIM
# ----------------------------------------------------------------------------------
1
1     {0:<4d}     {1:<4d}      {2:<4d}

# ==================================================================================
# Type               B1  F1    S1   E1   S2   E2   B2  F2   S1   E1   S2   E2   Swap
# ----------------------------------------------------------------------------------

'symmetry_z_strong'   1   1     1   {0:<4d}    1   {1:<4d}
'symmetry_z_strong'   1   2     1   {0:<4d}    1   {1:<4d}
'viscous_solid'       1   3     1   {1:<4d}    1   {2:<4d}
'viscous_solid'       1   4     1   {1:<4d}    1   {2:<4d}
'viscous_solid'       1   5     1   {2:<4d}    1   {0:<4d}
'viscous_solid'       1   6     1   {2:<4d}    1   {0:<4d}
"""

with open('block.nmf', 'w') as nmf:
    nmf.write(nmf_content.format(len(x), len(y), len(z)))
