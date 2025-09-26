# Magnetic Spiral Structure Generator

A Python script for generating 3D magnetic spiral structures and exporting them to XSF format for visualization in VESTA (Visualization for Electronic and STructural Analysis).

## Overview

This tool creates magnetic spiral structures commonly found in frustrated magnetic systems, antiferromagnetic materials, and complex magnetic phases. The script calculates magnetic moment orientations based on a spiral wave vector and exports the structure for 3D visualization.

## Features

- Generate 3D magnetic spiral structures with customizable parameters
- Calculate magnetic moment vectors using spiral wave vector formalism
- Compute angles between magnetic moments for analysis
- Export to XSF format compatible with VESTA
- Console output with detailed structure information
- Modular, well-documented code structure

## Requirements

- Python 3.6+
- NumPy
- VESTA (for visualization, optional)

## Installation

1. Ensure Python and NumPy are installed:
   ```bash
   pip install numpy
   ```

2. Download the script:
   ```bash
   # Save the script as spiral-3d-v4-xsf-claude.py
   ```

3. Make it executable (optional):
   ```bash
   chmod +x spiral-3d-v4-xsf-claude.py
   ```

## Usage

### Basic Usage

Run the script with default parameters:

```bash
python spiral-3d-v4-xsf-claude.py
```

This will:
- Generate a magnetic spiral structure
- Print structure information to console
- Create `spiral.xsf` file in the same directory

### Customization

Modify parameters in the `main()` function:

```python
def main():
    # Number of atoms for one complete spiral cycle
    atoms_in_spiral = 3
    
    # Spiral wave vector [qx, qy, qz]
    q = [0, 0.5 - 0.5 * (1/atoms_in_spiral), 0.5 - 0.5 * (1/atoms_in_spiral)]
    
    # Initial magnetization direction [mx, my, mz]
    m_1 = [1, 0, 0]  # Along x-axis
    
    # Supercell size [nx, ny, nz]
    R_max = [atoms_in_spiral, atoms_in_spiral * 2, atoms_in_spiral * 2]
```

## Parameters Explained

### Core Parameters

- **`atoms_in_spiral`**: Number of atoms required for the spiral to complete one full cycle along one axis
- **`q` (spiral wave vector)**: Defines the spiral periodicity in reciprocal space
  - Format: `[qx, qy, qz]`
  - Common values: `[0, 0.5, 0.5]` for simple spirals
- **`m_1` (initial moment)**: Starting magnetic moment direction
  - Format: `[mx, my, mz]`
  - Normalized automatically during calculation
- **`R_max` (supercell)**: Dimensions of the generated structure
  - Format: `[nx, ny, nz]` unit cells

### Output Parameters

- **`scale`**: Distance scaling factor between atoms in XSF file (default: 3 Ångströms)
- **`filename`**: Output XSF filename (default: "spiral.xsf")

## Mathematical Background

The magnetic moment at position **R** = (i, j, k) is calculated using:

```
M(R) = M₀ × [cos(q·R × 2π), sin(q·R × 2π), mz]
```

Where:
- **q·R** = qx×i + qy×j + qz×k (dot product)
- **M₀** = initial magnetic moment vector
- The rotation occurs in the xy-plane while preserving the z-component

## Output Files

### XSF File Structure

The generated XSF file contains:
- **CRYSTAL**: Crystal structure definition
- **PRIMVEC**: Unit cell vectors (scaled cubic cell)
- **PRIMCOORD**: Atomic positions with magnetic moments
  - Element 26 (Iron) used as default magnetic atom
  - Position coordinates (x, y, z)
  - Magnetic moment components (mx, my, mz)

### Console Output

Example output:
```
Spiral vector q = [0, 0.333, 0.333]
Initial moment = [1, 0, 0]
Supercell dimensions = [3, 6, 6]
Generated 108 atomic positions

Position (i,j,k) | Magnetic Moment (mx,my,mz) | Angle (deg)
-----------------------------------------------------------------
 0  0  0 |   1.000   0.000   0.000 |    0.000
 0  0  1 |   0.500   0.866   0.000 |   60.000
 0  0  2 |  -0.500   0.866   0.000 |  120.000
...
```

## Visualization in VESTA

1. **Open VESTA**
2. **Load structure**: File → Open → Select `spiral.xsf`
3. **Enable vectors**: Properties → Vector
4. **Adjust display**:
   - Vector scale: Adjust size of magnetic moment arrows
   - Colors: Customize atom and vector colors
   - View: Rotate and zoom to examine spiral structure

### VESTA Tips

- Use **Edit → Boundary** to show unit cell
- **View → Projection** for different viewing angles
- **Properties → Atoms** to modify atom appearance
- **Properties → Vector → Scale** to adjust arrow sizes

## Common Spiral Types

### Simple Helical Spiral
```python
atoms_in_spiral = 4
q = [0, 0, 0.25]  # Spiral along z-axis
m_1 = [1, 0, 0]   # Start along x
```

### Cycloidal Spiral
```python
atoms_in_spiral = 6
q = [0, 0.167, 0]  # Spiral in yz-plane
m_1 = [0, 1, 0]    # Start along y
```

### Complex 3D Spiral
```python
atoms_in_spiral = 8
q = [0.125, 0.125, 0.125]  # 3D spiral
m_1 = [1/√2, 1/√2, 0]      # 45° initial angle
```

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure NumPy is installed
   ```bash
   pip install numpy
   ```

2. **File Not Created**: Check write permissions in script directory

3. **VESTA Can't Open File**: Verify XSF format by checking file contents

4. **Unexpected Spiral Pattern**: 
   - Check `atoms_in_spiral` matches desired periodicity
   - Verify spiral vector `q` components
   - Ensure `R_max` is large enough to show full pattern

### Validation

- Verify spiral periodicity: magnetic moments should repeat after `atoms_in_spiral` steps
- Check angle calculations: angles should follow expected spiral progression
- Visual inspection in VESTA: spiral should form smooth helical pattern

## Applications

- **Magnetic structure analysis**: Study complex magnetic phases
- **Educational purposes**: Visualize magnetic spiral concepts
- **Research**: Generate input structures for magnetic simulations
- **Material science**: Investigate frustrated magnetic systems

## File Structure

```
project-directory/
├── spiral-3d-v4-xsf-claude.py    # Main script
├── spiral.xsf                    # Generated XSF file
└── README.md                     # This file
```

## Contributing

To modify or extend the script:
1. Functions are well-documented with docstrings
2. Parameters are centralized in the `main()` function
3. Core logic is in `generate_spiral_structure()`
4. XSF output is handled by `create_xsf_file()`

## References

- VESTA: K. Momma and F. Izumi, "VESTA 3 for three-dimensional visualization of crystal, volumetric and morphology data," J. Appl. Crystallogr. 44, 1272-1276 (2011)
- XSF Format: XCrySDen file format specification
- Magnetic spirals: See standard solid-state physics and magnetism textbooks

## License

This script is provided as-is for educational and research purposes.
