@echo off

echo Checking Docker connection...
docker version >nul 2>&1
if errorlevel 1 (
    echo Docker is not available. Please start Docker and try again.
    pause
    exit /b 1
)
echo Docker is available.

REM Move to infra\Docker for building images and pushing
cd /d "%~dp0..\infra\Docker"
if not exist docker-compose.yml (
    echo docker-compose.yml NOT FOUND in infra\Docker. Check your files and try again.
    pause
    exit /b 1
)

echo Building all images with docker-compose...
docker-compose build
if errorlevel 1 (
    echo Build failed. Please check docker-compose.yml and try again.
    pause
    exit /b 1
)

echo Pushing all images to Docker Hub...
docker-compose push
if errorlevel 1 (
    echo Push failed. Please check login status and try again.
    pause
    exit /b 1
)

REM Back to scriptes folder (where the .bat is)
cd /d "%~dp0"
oc login --token=sha256~oTRYp523ZYX2j6kPcux8EFSc1ysJ_JobVGnhmBVzyr8 --server=https://api.rm2.thpm.p1.openshiftapps.com:6443
echo Deploying Kubernetes YAMLs...
oc apply -f ../infra/open-shift
if errorlevel 1 (
    echo YAML deployment failed. Check YAML files.
    pause
    exit /b 1
)

echo All steps completed successfully!
pause
