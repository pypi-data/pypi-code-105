import orekit
from numpy import deg2rad
from orekit import JArray_double
from orekit.pyhelpers import setup_orekit_curdir
from org.hipparchus.geometry.euclidean.threed import RotationOrder, Vector3D
from org.hipparchus.ode.nonstiff import DormandPrince853Integrator
from org.orekit.bodies import (
    CelestialBody,
    CelestialBodyFactory,
    GeodeticPoint,
    OneAxisEllipsoid,
)
from org.orekit.forces import BoxAndSolarArraySpacecraft
from org.orekit.forces.drag import DragForce, IsotropicDrag
from org.orekit.forces.gravity import HolmesFeatherstoneAttractionModel
from org.orekit.forces.gravity.potential import GravityFieldFactory
from org.orekit.frames import FramesFactory, ITRFVersion, LOFType, TopocentricFrame
from org.orekit.models.earth.atmosphere import DTM2000, JB2008
from org.orekit.models.earth.atmosphere.data import (
    MarshallSolarActivityFutureEstimation,
)
from org.orekit.orbits import (
    EquinoctialOrbit,
    KeplerianOrbit,
    Orbit,
    OrbitType,
    PositionAngle,
)
from org.orekit.propagation import SpacecraftState
from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.utils import Constants, IERSConventions, PVCoordinatesProvider

orekit.initVM()
setup_orekit_curdir()


def create_initial_state(orbit, satellite_mass=0.):
    return SpacecraftState(orbit, satellite_mass)


def get_earth_shape(r=Constants.WGS84_EARTH_EQUATORIAL_RADIUS,
                    f=Constants.WGS84_EARTH_FLATTENING):
    itrf = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
    return OneAxisEllipsoid(r, f, itrf)


def create_gravity_field(propagator, nzon, ntess):
    """Create gravity field force instance"""
    earth_shape = get_earth_shape()
    gravity_provider = GravityFieldFactory.getNormalizedProvider(nzon, ntess)
    propagator.addForceModel(HolmesFeatherstoneAttractionModel(earth_shape.getBodyFrame(), gravity_provider))


def create_atmosphere(level):
    """create DTM2000 atmosphere"""
    earth_shape = get_earth_shape()
    sun = CelestialBodyFactory.getSun()
    parameters = MarshallSolarActivityFutureEstimation(MarshallSolarActivityFutureEstimation.DEFAULT_SUPPORTED_NAMES, level)
    atm = DTM2000(parameters, sun, earth_shape)
    return atm


def create_drag(propagator, dim, solar_array_curf, drag_coeff, solar_activity_level):
    """create drag force instance"""
    atm = create_atmosphere(solar_activity_level)
    absorption_coeff = 0.3
    reflection_coeff = 0.2
    sun = CelestialBodyFactory.getSun()
    sa_axis = Vector3D(0., 1., 0.)
    spacecraft = BoxAndSolarArraySpacecraft(dim, dim, dim,
                                            sun,
                                            solar_array_curf,
                                            sa_axis,
                                            drag_coeff, absorption_coeff, reflection_coeff)
    drag_force = DragForce(atm, spacecraft)
    propagator.addForceModel(drag_force)


# Propagator
def create_propagator(initial_state,
                      cross_section=None, solar_array_surf=0., drag_coeff=2.2,
                      solar_activity_level=MarshallSolarActivityFutureEstimation.StrengthLevel.AVERAGE,
                      n_zonal=8, n_tesseral=8):
    min_step = 0.001
    max_step = 600.0
    init_step = 60.0
    position_tolerance = 1.0
    orbit_type = OrbitType.CARTESIAN
    tol = NumericalPropagator.tolerances(position_tolerance,
                                         initial_state.getOrbit(), orbit_type)
    integrator = DormandPrince853Integrator(min_step, max_step,
                                            JArray_double.cast_(tol[0]),
                                            JArray_double.cast_(tol[1]))
    integrator.setInitialStepSize(init_step)
    propagator = NumericalPropagator(integrator)
    propagator.setOrbitType(orbit_type)
    propagator.setInitialState(initial_state)

    # gravity field
    create_gravity_field(propagator, n_zonal, n_tesseral)

    # drag
    if cross_section is not None:
        create_drag(propagator, cross_section, solar_array_surf, drag_coeff, solar_activity_level)

    return propagator
