set -x

cd ./python_pbs/extensions/pbs
source /etc/pbs.conf
echo "Configuring SWIG..."
swig -version

swig -python -I${PBS_EXEC}/include ./pbs_ifl.i

echo "Running GCC"
gcc -Wall -Wno-unused-variable -fPIC -shared -I${PBS_EXEC}/include -I$1 -L${PBS_EXEC}/lib -lpbs -o _pbs_ifl.so ./pbs_ifl_wrap.c
export LD_LIBRARY_PATH=${PBS_EXEC}/lib:${LD_LIBRARY_PATH}

ldd ./_pbs_ifl.so
cd ../../..