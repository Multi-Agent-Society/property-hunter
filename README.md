# property-hunter
A CrewAI architecture for filtering through rental property listings according to your specifications

## How to run project locally

1. Run the following command to build a docker image for the project:
```bash
docker build -t property-hunter .
```

2. Run this command to create and run a docker container linked to port 8080:
```bash
docker run -d -p 8080:8080 property-hunter
```

## How to set up conda environment (on MacOS/Linux)

1. Create a conda environment called `property-hunter` with Python 3.11.9.
```bash
conda create -n property-hunter python=3.11.9
```

2. Activate the conda environment you just created:
```bash
conda activate property-hunter
```

3. Install requirements with pip
```bash
pip install -r src/requirements.txt
```

## How to run example notebook (On Mac/Linux)

1. Update privileges on `config.sh` so that you can execute it:
```bash
chmod +x config.sh
```

2. Run `config.sh` shell file:
```bash
./config.sh
```

3. Repeat for `createmodel.sh`:
```bash
chmod +x createmodel.sh && ./createmodel.sh
```

4. Run the notebook!