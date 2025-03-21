# CAMulator_Figures

This repository contains figure generation scripts and Jupyter notebooks for the **CAMulator** publication. **CAMulator** is a machine-learning-based emulator of the Community Atmosphere Model version 6 (CAM6), designed to provide fast and accurate climate simulations.

## 📌 About
This repository is specifically for generating figures related to the **CAMulator** study and its evaluation. If you are looking for the **CAMulator** model itself, please refer to the main repository (**[Link to Repo](https://github.com/NCAR/miles-credit/tree/climate_runs)**).

## 📂 Repository Structure
```
CAMulator_Figures/
│── Figure_Notebooks/        # Jupyter notebooks for figure generation
│── README.md                # This file
```

## 📊 Figures Overview
The notebooks in this repository generate key figures from the **CAMulator** study, including:
- **Model climatology comparisons** (CAMulator vs. CAM6)
- **Modes of climate variability** (ENSO, NAO, PNA)
- **Precipitation and temperature biases**
- **Extreme events and variability**
- **+2K and +4K SST warming response**
- **Global conservation properties (mass, moisture, and energy)**

## 📜 How to Use
### Prerequisites
Ensure you have Python and Jupyter Notebook installed. The required dependencies can be installed using:

#### Standard Installation From CREDIT REPO
Clone from miles-credit github page:
```bash
# needed an sshkey to use this command: git clone git@github.com:NCAR/miles-credit.git
git clone https://github.com/NCAR/miles-credit.git
cd miles-credit
```

Install dependencies using environment_gpu.yml file (also compatible with CPU-only machines):

Note: if you are on NCAR HPC, we recommend installing to your home directory. To do this, simply append `-p /glade/u/home/$USER/[your_install_dir]/` to the `conda/mamba env create` command below:

```bash
mamba env create -f environment_gpu.yml
conda activate credit
```

CPU-only install:
```bash
mamba env create -f environment_cpu.yml
conda activate credit
```


Some metrics use WeatherBench2 for computation. Install with:
```bash
git clone git@github.com:google-research/weatherbench2.git
cd weatherbench2
pip install .
````

### Running the Notebooks
To generate the figures, clone the repository and run the notebooks:
```bash
git clone https://github.com/yourusername/CAMulator_Figures.git
cd CAMulator_Figures/Figure_Notebooks
jupyter notebook
```
Open the relevant notebook and run the cells to generate the figures.

## 🏗 Future Work
- Automate figure generation with a Python script.
- Improve visualization aesthetics.
- Include interactive visualizations.

## 🔗 Related Repositories
- **[CAMulator Model Repository](https://github.com/NCAR/miles-credit/tree/climate_runs)**

## 📄 Citation
If you use **CAMulator** or figures from this repository in your research, please cite the corresponding publication:

> Chapman, W. et al. *Fully Resolved, Fast Emulation of the Community Atmosphere Model (CAM6)*, 2025. [arXiv link]

## 🤝 Contributing
Contributions and suggestions are welcome! Feel free to submit a pull request or open an issue.

---

Would you like me to tailor this further with installation guides, dataset links, or specific notebook descriptions? 🚀
