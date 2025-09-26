"""
Magnetic Spiral Structure Generator
Creates 3D magnetic spiral structures and exports to XSF format for VESTA visualization
"""

import numpy as np
import os


def generate_spiral_structure(atoms_in_spiral, R_max, q_vector, initial_moment):
    """
    Generate magnetic spiral structure with specified parameters

    Args:
        atoms_in_spiral: Number of atoms for spiral to complete one cycle
        R_max: Supercell dimensions [x, y, z]
        q_vector: Spiral wave vector [qx, qy, qz]
        initial_moment: Initial magnetization vector [mx, my, mz]

    Returns:
        tuple: (positions, magnetic_moments, angles)
    """
    # Generate atomic positions
    positions = []
    magnetic_moments = []
    angles = []

    num = 0
    for i in range(R_max[0]):
        for j in range(R_max[1]):
            for k in range(R_max[2]):
                # Store position
                positions.append([i, j, k])

                # Calculate phase for this position
                phase = (q_vector[0] * i + q_vector[1] * j + q_vector[2] * k) * 2 * np.pi

                # Calculate magnetic moment components using rotation matrix
                mx = (initial_moment[0] * np.cos(phase) -
                      initial_moment[1] * np.sin(phase))
                my = (initial_moment[0] * np.sin(phase) +
                      initial_moment[1] * np.cos(phase))
                mz = initial_moment[2]

                magnetic_moments.append([mx, my, mz])

                # Calculate angle with respect to first moment
                if num == 0:
                    angle_deg = 0.0
                else:
                    dot_product = (mx * magnetic_moments[0][0] +
                                   my * magnetic_moments[0][1] +
                                   mz * magnetic_moments[0][2])

                    mag_current = np.sqrt(mx ** 2 + my ** 2 + mz ** 2)
                    mag_first = np.sqrt(sum(m ** 2 for m in magnetic_moments[0]))

                    if mag_current * mag_first == 0:
                        angle_deg = 0.0
                    else:
                        cos_angle = dot_product / (mag_current * mag_first)
                        cos_angle = np.clip(cos_angle, -1.0, 1.0)
                        angle_deg = np.arccos(cos_angle) * 180 / np.pi

                angles.append(angle_deg)
                num += 1

    return positions, magnetic_moments, angles


def print_structure_info(positions, magnetic_moments, angles):
    """Print structure information to console"""
    print(f"Generated {len(positions)} atomic positions")
    print("\nPosition (i,j,k) | Magnetic Moment (mx,my,mz) | Angle (deg)")
    print("-" * 65)

    for i, (pos, mom, angle) in enumerate(zip(positions, magnetic_moments, angles)):
        print(f"{pos[0]:2d} {pos[1]:2d} {pos[2]:2d} | "
              f"{mom[0]:7.3f} {mom[1]:7.3f} {mom[2]:7.3f} | "
              f"{angle:8.3f}")


def create_xsf_file(positions, magnetic_moments, R_max, filename="spiral.xsf", scale=3):
    """
    Create XSF file for VESTA visualization

    Args:
        positions: List of atomic positions
        magnetic_moments: List of magnetic moment vectors
        R_max: Supercell dimensions
        filename: Output filename
        scale: Scaling factor for unit cell and positions
    """
    # Get script directory for file saving
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    with open(filepath, 'w') as f:
        # XSF header
        f.write("# XSF file generated for magnetic spiral visualization\n")
        f.write("# Can be opened in VESTA to visualize magnetic moments\n")
        f.write("CRYSTAL\n")

        # Define unit cell vectors
        f.write("PRIMVEC\n")
        f.write(f"{R_max[0] * scale:6.1f}  0.0  0.0\n")
        f.write(f"  0.0  {R_max[1] * scale:6.1f}  0.0\n")
        f.write(f"  0.0  0.0  {R_max[2] * scale:6.1f}\n")

        # Write atomic coordinates
        f.write("PRIMCOORD\n")
        f.write(f"{len(positions)} 1\n")

        for pos, mom in zip(positions, magnetic_moments):
            x, y, z = pos[0] * scale, pos[1] * scale, pos[2] * scale
            mx, my, mz = mom[0] * scale, mom[1] * scale, mom[2] * scale

            # Element 26 (Fe) with position and magnetic moment
            f.write(f"26  {x:8.4f}  {y:8.4f}  {z:8.4f}  "
                    f"{mx:8.4f}  {my:8.4f}  {mz:8.4f}\n")

        f.write("\n")

    print(f"\nXSF file '{filename}' created successfully!")
    print(f"File saved at: {filepath}")
    print("\nTo visualize in VESTA:")
    print("1. Open VESTA")
    print(f"2. File -> Open -> Select the XSF file")
    print("3. Properties -> Vector to display magnetic moment vectors")
    print("4. Adjust vector scaling and colors as needed")


def main():
    """Main function to generate magnetic spiral structure"""
    # Configuration parameters
    # q-wavevector can be defined by numbers of atoms which form a complete spiral  cycle along 1 axis
    atoms_in_spiral = 3

    # Spiral wave vector
    q = [0, 0.5 - 0.5 * (1 / atoms_in_spiral), 0.5 - 0.5 * (1 / atoms_in_spiral)]
    print(f"Spiral vector q = {q}")

    # Initial magnetization vector
    m_1 = [1, 0, 0]  # Default: along x-axis
    print(f"Initial moment = {m_1}")

    # Supercell dimensions [x, y, z]
    R_max = [atoms_in_spiral, atoms_in_spiral * 2, atoms_in_spiral * 2]
    print(f"Supercell dimensions = {R_max}")

    # Generate spiral structure
    positions, magnetic_moments, angles = generate_spiral_structure(
        atoms_in_spiral, R_max, q, m_1)

    # Print structure information
    print_structure_info(positions, magnetic_moments, angles)

    # Create XSF file for VESTA
    # scale parameter defines a distance between atoms
    create_xsf_file(positions, magnetic_moments, R_max, "spiral.xsf", scale=3)


if __name__ == "__main__":
    main()