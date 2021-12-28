# -*- coding: utf-8 -*-
"""
Simple transfer example to generate OEM and AEM files.

@author: Joris Olympio
"""

from datetime import timedelta
from math import radians

import numpy as np
import orekit
from java.lang import StringBuilder
from java.util import ArrayList as ArrayList
from java.util import Collections
from oacmpy.ccsds.Cdm import Cdm
from oacmpy.ccsds.enumerates import ConjunctionObject
from oacmpy.ccsds.Oem import Oem
from oacmpy.czml.CdmToCzml import CdmToCzml
from oacmpy.czml.OemToCzml import OemAemToCzml
from oacmpy.czml.ScenarioCzml import ScenarioCzml
from orekit import JArray_double
from orekit.pyhelpers import setup_orekit_curdir
from org.hipparchus.geometry.euclidean.threed import RotationOrder, Vector3D
from org.hipparchus.ode.nonstiff import DormandPrince853Integrator
from org.orekit.attitudes import LofOffset
from org.orekit.bodies import (
    CelestialBody,
    CelestialBodyFactory,
    GeodeticPoint,
    OneAxisEllipsoid,
)
from org.orekit.files.ccsds import OEMWriter  # , AEMWriter
from org.orekit.files.general import OrekitEphemerisFile
from org.orekit.forces import BoxAndSolarArraySpacecraft
from org.orekit.forces.drag import DragForce, IsotropicDrag
from org.orekit.forces.gravity import HolmesFeatherstoneAttractionModel
from org.orekit.forces.gravity.potential import GravityFieldFactory
from org.orekit.frames import FramesFactory, ITRFVersion, LOFType, TopocentricFrame
from org.orekit.models.earth.atmosphere import DTM2000, JB2008
from org.orekit.models.earth.atmosphere.data import (
    MarshallSolarActivityFutureEstimation,
)
from org.orekit.orbits import CartesianOrbit, Orbit, OrbitType, PositionAngle
from org.orekit.propagation import SpacecraftState
from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.utils import (
    Constants,
    IERSConventions,
    PVCoordinates,
    PVCoordinatesProvider,
)

print("Initialising Orekit")
orekit.initVM()
setup_orekit_curdir()


utc = TimeScalesFactory.getUTC()
mu = Constants.WGS84_EARTH_MU

frame = FramesFactory.getEME2000()

satellite_mass = 2000.0  # kg
crossSection = 2.5  # m2
solarArraySurf = 2 * 16 * 6.0  # m2
dragCoeff = 2.2
step_time = 30.0  # s


def create_initial_state(orbit, satellite_mass=0.0):
    return SpacecraftState(orbit, satellite_mass)


def get_earth_shape(
    r=Constants.WGS84_EARTH_EQUATORIAL_RADIUS, f=Constants.WGS84_EARTH_FLATTENING
):
    itrf = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
    return OneAxisEllipsoid(r, f, itrf)


def create_gravity_field(propagator, nzon, ntess):
    """Create gravity field force instance"""
    earth_shape = get_earth_shape()
    gravity_provider = GravityFieldFactory.getNormalizedProvider(nzon, ntess)
    propagator.addForceModel(
        HolmesFeatherstoneAttractionModel(earth_shape.getBodyFrame(), gravity_provider)
    )


def create_atmosphere(level):
    """create DTM2000 atmosphere"""
    earth_shape = get_earth_shape()
    sun = CelestialBodyFactory.getSun()
    parameters = MarshallSolarActivityFutureEstimation(
        MarshallSolarActivityFutureEstimation.DEFAULT_SUPPORTED_NAMES, level
    )
    atm = DTM2000(parameters, sun, earth_shape)
    return atm


def create_drag(propagator, dim, solar_array_curf, drag_coeff, solar_activity_level):
    """create drag force instance"""
    atm = create_atmosphere(solar_activity_level)
    absorption_coeff = 0.3
    reflection_coeff = 0.2
    sun = CelestialBodyFactory.getSun()
    sa_axis = Vector3D(0.0, 1.0, 0.0)
    spacecraft = BoxAndSolarArraySpacecraft(
        dim,
        dim,
        dim,
        sun,
        solar_array_curf,
        sa_axis,
        drag_coeff,
        absorption_coeff,
        reflection_coeff,
    )
    drag_force = DragForce(atm, spacecraft)
    propagator.addForceModel(drag_force)


# Propagator
def create_propagator(
    initial_state,
    cross_section=None,
    solar_array_surf=0.0,
    drag_coeff=2.2,
    solar_activity_level=MarshallSolarActivityFutureEstimation.StrengthLevel.AVERAGE,
    n_zonal=8,
    n_tesseral=8,
):
    min_step = 0.001
    max_step = 600.0
    init_step = 60.0
    position_tolerance = 1.0
    orbit_type = OrbitType.CARTESIAN
    tol = NumericalPropagator.tolerances(
        position_tolerance, initial_state.getOrbit(), orbit_type
    )
    integrator = DormandPrince853Integrator(
        min_step, max_step, JArray_double.cast_(tol[0]), JArray_double.cast_(tol[1])
    )
    integrator.setInitialStepSize(init_step)
    propagator = NumericalPropagator(integrator)
    propagator.setOrbitType(orbit_type)
    propagator.setInitialState(initial_state)

    # gravity field
    create_gravity_field(propagator, n_zonal, n_tesseral)

    # drag
    if cross_section is not None:
        create_drag(
            propagator,
            cross_section,
            solar_array_surf,
            drag_coeff,
            solar_activity_level,
        )

    return propagator


def create_oem(
    i_object, object_name, datetime, state, prop_duration, duration_after_tca=0.0
):
    """create oem file"""
    position = Vector3D(state[0], state[1], state[2])
    velocity = Vector3D(state[3], state[4], state[5])
    pv = PVCoordinates(position, velocity)
    date = datetime.date()
    time = datetime.time()
    print("TCA: ", datetime)
    tca_date = AbsoluteDate(
        date.year, date.month, date.day, time.hour, time.minute, float(time.second), utc
    )

    initial_orbit = CartesianOrbit(pv, frame, tca_date, mu)

    # Attitude
    attitude_law = LofOffset(
        initial_orbit.getFrame(),
        LOFType.TNW,
        RotationOrder.XYZ,
        radians(0.0),
        radians(0.0),
        radians(0.0),
    )

    initial_state = create_initial_state(initial_orbit, satellite_mass)
    propagator = create_propagator(
        initial_state,
        cross_section=crossSection,
        solar_array_surf=solarArraySurf,
        drag_coeff=dragCoeff,
        n_zonal=6,
        n_tesseral=2,
    )
    propagator.setAttitudeProvider(attitude_law)

    print("Propagating")

    # Time array in orekit AbsoluteDate format
    tt = np.arange(duration_after_tca, prop_duration, -step_time)
    t = [tca_date.shiftedBy(float(dt)) for dt in tt]
    states = [propagator.propagate(x) for x in t]
    java_state_list = ArrayList()
    [java_state_list.add(s) for s in states]
    Collections.reverse(java_state_list)

    print("Generating OEM... ", object_name)
    ephemeris_file = OrekitEphemerisFile()
    satellite = ephemeris_file.addSatellite(object_name)
    satellite.addNewSegment(java_state_list)
    oem_writer = OEMWriter(
        OEMWriter.InterpolationMethod.LAGRANGE, "oacmPy", object_name, object_name
    )

    oem_str = StringBuilder()
    oem_writer.write(oem_str, ephemeris_file)
    filename = "sample_object{:d}.oem".format(i_object)
    with open(filename, "w") as f:
        f.write(oem_str.toString())
    return filename


def analyse_cdm(cdm_filename):
    cdm = Cdm(cdm_filename, "xml")
    date = cdm.get_tca().datetime

    primary_name = cdm.get_primary_satellite_name()
    state = cdm.get_state_vector(obj_name=ConjunctionObject.OBJECT1)
    filename1 = create_oem(1, primary_name, date, state, -45 * 60.0, 15 * 60.0)

    secondary_name = cdm.get_secondary_satellite_name()
    state = cdm.get_state_vector(obj_name=ConjunctionObject.OBJECT2)
    filename2 = create_oem(2, secondary_name, date, state, -45 * 60.0, 15 * 60.0)

    oem1 = Oem(filename1, "kvn")
    oem1_czml = OemAemToCzml(oem1)
    oem2 = Oem(filename2, "kvn")
    oem2_czml = OemAemToCzml(oem2)
    cdm = Cdm(cdm_filename, "xml")
    cdm_czml = CdmToCzml(cdm)
    cdm_czml.set_lead_time(timedelta(minutes=30))
    cdm_czml.set_scale(1.0)

    start = oem1.get_start_time(sat_name="SATELLITE A")
    end = oem1.get_stop_time(sat_name="SATELLITE A")
    print("Time frame: ", start, end)

    scenario = ScenarioCzml(start, end)
    scenario.add_content(oem1_czml)
    scenario.add_content(oem2_czml)
    scenario.add_content(cdm_czml)
    scenario.create_document("test_conjunction.czml")

    print("Done")


if __name__ == "__main__":
    cdm_filename = "test_cdm.xml"
    analyse_cdm(cdm_filename)
