
Instrucciones para la instalacion


Ambiente: 
sudo yum install python-virtualenv
sudo yum -y install gcc gcc-c++ kernel-devel
sudo yum -y install python-devel libxslt-devel libffi-devel openssl-devel

VirtualEnv
virtualenv purge_proy --python=python2.7
cd purge_proy
source ./bin/activate

Clonar el repositorio
git clone http://gitlabpro-d.cepal.org/uweb/purge.git <nombre-directorio>
pip install -r requeriments.txt

