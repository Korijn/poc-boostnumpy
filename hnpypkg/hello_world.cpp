#include <iostream>
#include "hello_world.h"
#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
 
namespace p = boost::python;
namespace np = boost::python::numpy;

BOOST_PYTHON_MODULE(hello_world)
{
	Py_Initialize();
	np::initialize();

	p::class_<HelloWorldSayer>("HelloWorldSayer", p::init<>())
		.def("SayHello", &HelloWorldSayer::SayHello)
		;
}
 
void HelloWorldSayer::SayHello() 
{
	p::tuple shape = p::make_tuple(3, 3);
	np::dtype dtype = np::dtype::get_builtin<float>();
	np::ndarray a = np::zeros(shape, dtype);

	std::cout << "Original array:\n" << p::extract<char const *>(p::str(a)) << std::endl;

	// Reshape the array into a 1D array
	a = a.reshape(p::make_tuple(9));
	// Print it again.
	std::cout << "Reshaped array:\n" << p::extract<char const *>(p::str(a)) << std::endl;
}