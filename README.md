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