"""
Main routine to tag files

This is a utility that will create a tags file readable by ViM for an IDF file
Because ctags expects proper variable names (no spaces, special characters,
etc), we have to create a new IDF file with these special characters removed

"""

import os
import glob as gb
import sys  # for compatilbity

# Because find_non_reference_classes relies on Eppy, it's slow, so I hardcode
# the classes names that aren't a reference object.
NOT_REFERENCE_CLASSES = [
    'AIRCONDITIONER:VARIABLEREFRIGERANTFLOW:FLUIDTEMPERATURECONTROL',
    'AIRCONDITIONER:VARIABLEREFRIGERANTFLOW:FLUIDTEMPERATURECONTROL:HR',
    'AIRFLOWNETWORK:DISTRIBUTION:DUCTVIEWFACTORS',
    'AIRFLOWNETWORK:DISTRIBUTION:LINKAGE',
    'AIRFLOWNETWORK:MULTIZONE:SURFACE',
    'AIRFLOWNETWORK:SIMULATIONCONTROL',
    'AIRLOOPHVAC:RETURNPATH',
    'AIRLOOPHVAC:SUPPLYPATH',
    'BUILDING',
    'COIL:WATERHEATING:DESUPERHEATER',
    'COMPLEXFENESTRATIONPROPERTY:SOLARABSORBEDLAYERS',
    'COMPLIANCE:BUILDING',
    'COMPONENTCOST:ADJUSTMENTS',
    'COMPONENTCOST:LINEITEM',
    'COMPONENTCOST:REFERENCE',
    'CONNECTOR:MIXER',
    'CONNECTOR:SPLITTER',
    'CONVERGENCELIMITS',
    'CURRENCYTYPE',
    'DAYLIGHTING:CONTROLS',
    'DAYLIGHTING:DELIGHT:COMPLEXFENESTRATION',
    'DAYLIGHTINGDEVICE:LIGHTWELL',
    'DAYLIGHTINGDEVICE:SHELF',
    'DAYLIGHTINGDEVICE:TUBULAR',
    'DEMANDMANAGERASSIGNMENTLIST',
    'ELECTRICEQUIPMENT:ITE:AIRCOOLED',
    'ELECTRICLOADCENTER:DISTRIBUTION',
    'ENERGYMANAGEMENTSYSTEM:ACTUATOR',
    'ENERGYMANAGEMENTSYSTEM:CONSTRUCTIONINDEXVARIABLE',
    'ENERGYMANAGEMENTSYSTEM:CURVEORTABLEINDEXVARIABLE',
    'ENERGYMANAGEMENTSYSTEM:GLOBALVARIABLE',
    'ENERGYMANAGEMENTSYSTEM:INTERNALVARIABLE',
    'ENERGYMANAGEMENTSYSTEM:METEREDOUTPUTVARIABLE',
    'ENERGYMANAGEMENTSYSTEM:OUTPUTVARIABLE',
    'ENERGYMANAGEMENTSYSTEM:SENSOR',
    'ENERGYMANAGEMENTSYSTEM:TRENDVARIABLE',
    'ENVIRONMENTALIMPACTFACTORS',
    'EXTERIOR:FUELEQUIPMENT',
    'EXTERIOR:WATEREQUIPMENT',
    'EXTERNALINTERFACE',
    'EXTERNALINTERFACE:ACTUATOR',
    'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITEXPORT:FROM:VARIABLE',
    'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITEXPORT:TO:ACTUATOR',
    'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITEXPORT:TO:VARIABLE',
    'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITIMPORT:FROM:VARIABLE',
    'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITIMPORT:TO:ACTUATOR',
    'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITIMPORT:TO:VARIABLE',
    'EXTERNALINTERFACE:VARIABLE',
    'FANPERFORMANCE:NIGHTVENTILATION',
    'FAULTMODEL:ENTHALPYSENSOROFFSET:OUTDOORAIR',
    'FAULTMODEL:ENTHALPYSENSOROFFSET:RETURNAIR',
    'FAULTMODEL:FOULING:AIRFILTER',
    'FAULTMODEL:FOULING:BOILER',
    'FAULTMODEL:FOULING:CHILLER',
    'FAULTMODEL:FOULING:COIL',
    'FAULTMODEL:FOULING:COOLINGTOWER',
    'FAULTMODEL:FOULING:EVAPORATIVECOOLER',
    'FAULTMODEL:HUMIDISTATOFFSET',
    'FAULTMODEL:HUMIDITYSENSOROFFSET:OUTDOORAIR',
    'FAULTMODEL:PRESSURESENSOROFFSET:OUTDOORAIR',
    'FAULTMODEL:TEMPERATURESENSOROFFSET:CHILLERSUPPLYWATER',
    'FAULTMODEL:TEMPERATURESENSOROFFSET:COILSUPPLYAIR',
    'FAULTMODEL:TEMPERATURESENSOROFFSET:CONDENSERSUPPLYWATER',
    'FAULTMODEL:TEMPERATURESENSOROFFSET:OUTDOORAIR',
    'FAULTMODEL:TEMPERATURESENSOROFFSET:RETURNAIR',
    'FLUIDPROPERTIES:CONCENTRATION',
    'FLUIDPROPERTIES:GLYCOLCONCENTRATION',
    'FLUIDPROPERTIES:SATURATED',
    'FLUIDPROPERTIES:SUPERHEATED',
    'FOUNDATION:KIVA:SETTINGS',
    'FUELFACTORS',
    'GASEQUIPMENT',
    'GEOMETRYTRANSFORM',
    'GLOBALGEOMETRYRULES',
    'GROUNDHEATTRANSFER:BASEMENT:AUTOGRID',
    'GROUNDHEATTRANSFER:BASEMENT:BLDGDATA',
    'GROUNDHEATTRANSFER:BASEMENT:COMBLDG',
    'GROUNDHEATTRANSFER:BASEMENT:EQUIVAUTOGRID',
    'GROUNDHEATTRANSFER:BASEMENT:EQUIVSLAB',
    'GROUNDHEATTRANSFER:BASEMENT:INSULATION',
    'GROUNDHEATTRANSFER:BASEMENT:INTERIOR',
    'GROUNDHEATTRANSFER:BASEMENT:MANUALGRID',
    'GROUNDHEATTRANSFER:BASEMENT:MATLPROPS',
    'GROUNDHEATTRANSFER:BASEMENT:SIMPARAMETERS',
    'GROUNDHEATTRANSFER:BASEMENT:SURFACEPROPS',
    'GROUNDHEATTRANSFER:BASEMENT:XFACE',
    'GROUNDHEATTRANSFER:BASEMENT:YFACE',
    'GROUNDHEATTRANSFER:BASEMENT:ZFACE',
    'GROUNDHEATTRANSFER:CONTROL',
    'GROUNDHEATTRANSFER:SLAB:AUTOGRID',
    'GROUNDHEATTRANSFER:SLAB:BLDGPROPS',
    'GROUNDHEATTRANSFER:SLAB:BOUNDCONDS',
    'GROUNDHEATTRANSFER:SLAB:EQUIVALENTSLAB',
    'GROUNDHEATTRANSFER:SLAB:INSULATION',
    'GROUNDHEATTRANSFER:SLAB:MANUALGRID',
    'GROUNDHEATTRANSFER:SLAB:MATERIALS',
    'GROUNDHEATTRANSFER:SLAB:MATLPROPS',
    'GROUNDHEATTRANSFER:SLAB:XFACE',
    'GROUNDHEATTRANSFER:SLAB:YFACE',
    'GROUNDHEATTRANSFER:SLAB:ZFACE',
    'HEATBALANCEALGORITHM',
    'HEATBALANCESETTINGS:CONDUCTIONFINITEDIFFERENCE',
    'HOTWATEREQUIPMENT',
    'HVACTEMPLATE:PLANT:BOILER',
    'HVACTEMPLATE:PLANT:BOILER:OBJECTREFERENCE',
    'HVACTEMPLATE:PLANT:CHILLEDWATERLOOP',
    'HVACTEMPLATE:PLANT:CHILLER',
    'HVACTEMPLATE:PLANT:CHILLER:OBJECTREFERENCE',
    'HVACTEMPLATE:PLANT:HOTWATERLOOP',
    'HVACTEMPLATE:PLANT:MIXEDWATERLOOP',
    'HVACTEMPLATE:PLANT:TOWER',
    'HVACTEMPLATE:PLANT:TOWER:OBJECTREFERENCE',
    'HVACTEMPLATE:ZONE:BASEBOARDHEAT',
    'HVACTEMPLATE:ZONE:DUALDUCT',
    'HVACTEMPLATE:ZONE:FANCOIL',
    'HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM',
    'HVACTEMPLATE:ZONE:PTAC',
    'HVACTEMPLATE:ZONE:PTHP',
    'HVACTEMPLATE:ZONE:UNITARY',
    'HVACTEMPLATE:ZONE:VAV',
    'HVACTEMPLATE:ZONE:VAV:FANPOWERED',
    'HVACTEMPLATE:ZONE:VAV:HEATANDCOOL',
    'HVACTEMPLATE:ZONE:VRF',
    'HVACTEMPLATE:ZONE:WATERTOAIRHEATPUMP',
    'HYBRIDMODEL:ZONE',
    'LEAD INPUT',
    'LIFECYCLECOST:NONRECURRINGCOST',
    'LIFECYCLECOST:PARAMETERS',
    'LIFECYCLECOST:RECURRINGCOSTS',
    'LIFECYCLECOST:USEADJUSTMENT',
    'LIFECYCLECOST:USEPRICEESCALATION',
    'MATERIALPROPERTY:HEATANDMOISTURETRANSFER:DIFFUSION',
    'MATERIALPROPERTY:HEATANDMOISTURETRANSFER:REDISTRIBUTION',
    'MATERIALPROPERTY:HEATANDMOISTURETRANSFER:SETTINGS',
    'MATERIALPROPERTY:HEATANDMOISTURETRANSFER:SORPTIONISOTHERM',
    'MATERIALPROPERTY:HEATANDMOISTURETRANSFER:SUCTION',
    'MATERIALPROPERTY:HEATANDMOISTURETRANSFER:THERMALCONDUCTIVITY',
    'MATERIALPROPERTY:MOISTUREPENETRATIONDEPTH:SETTINGS',
    'MATERIALPROPERTY:PHASECHANGE',
    'MATERIALPROPERTY:VARIABLETHERMALCONDUCTIVITY',
    'METER:CUSTOM',
    'METER:CUSTOMDECREMENT',
    'NODELIST',
    'OTHEREQUIPMENT',
    'OUTDOORAIR:NODE',
    'OUTDOORAIR:NODELIST',
    'OUTPUT:CONSTRUCTIONS',
    'OUTPUT:DAYLIGHTFACTORS',
    'OUTPUT:DEBUGGINGDATA',
    'OUTPUT:DIAGNOSTICS',
    'OUTPUT:ENERGYMANAGEMENTSYSTEM',
    'OUTPUT:ENVIRONMENTALIMPACTFACTORS',
    'OUTPUT:ILLUMINANCEMAP',
    'OUTPUT:METER',
    'OUTPUT:METER:CUMULATIVE',
    'OUTPUT:METER:CUMULATIVE:METERFILEONLY',
    'OUTPUT:METER:METERFILEONLY',
    'OUTPUT:PREPROCESSORMESSAGE',
    'OUTPUT:SCHEDULES',
    'OUTPUT:SQLITE',
    'OUTPUT:SURFACES:DRAWING',
    'OUTPUT:SURFACES:LIST',
    'OUTPUT:TABLE:ANNUAL',
    'OUTPUT:TABLE:MONTHLY',
    'OUTPUT:TABLE:SUMMARYREPORTS',
    'OUTPUT:TABLE:TIMEBINS',
    'OUTPUT:VARIABLE',
    'OUTPUT:VARIABLEDICTIONARY',
    'OUTPUTCONTROL:ILLUMINANCEMAP:STYLE',
    'OUTPUTCONTROL:REPORTINGTOLERANCES',
    'OUTPUTCONTROL:SIZING:STYLE',
    'OUTPUTCONTROL:TABLE:STYLE',
    'PARAMETRIC:FILENAMESUFFIX',
    'PARAMETRIC:LOGIC',
    'PARAMETRIC:RUNCONTROL',
    'PARAMETRIC:SETVALUEFORRUN',
    'PIPINGSYSTEM:UNDERGROUND:DOMAIN',
    'PLANTEQUIPMENTOPERATION:USERDEFINED',
    'ROOFIRRIGATION',
    'ROOMAIR:TEMPERATUREPATTERN:CONSTANTGRADIENT',
    'ROOMAIR:TEMPERATUREPATTERN:NONDIMENSIONALHEIGHT',
    'ROOMAIR:TEMPERATUREPATTERN:SURFACEMAPPING',
    'ROOMAIR:TEMPERATUREPATTERN:TWOGRADIENT',
    'ROOMAIR:TEMPERATUREPATTERN:USERDEFINED',
    'ROOMAIRMODELTYPE',
    'ROOMAIRSETTINGS:AIRFLOWNETWORK',
    'ROOMAIRSETTINGS:CROSSVENTILATION',
    'ROOMAIRSETTINGS:ONENODEDISPLACEMENTVENTILATION',
    'ROOMAIRSETTINGS:THREENODEDISPLACEMENTVENTILATION',
    'ROOMAIRSETTINGS:UNDERFLOORAIRDISTRIBUTIONEXTERIOR',
    'ROOMAIRSETTINGS:UNDERFLOORAIRDISTRIBUTIONINTERIOR',
    'RUNPERIODCONTROL:DAYLIGHTSAVINGTIME',
    'RUNPERIODCONTROL:SPECIALDAYS',
    'SETPOINTMANAGER:COLDEST',
    'SETPOINTMANAGER:CONDENSERENTERINGRESET',
    'SETPOINTMANAGER:CONDENSERENTERINGRESET:IDEAL',
    'SETPOINTMANAGER:FOLLOWGROUNDTEMPERATURE',
    'SETPOINTMANAGER:FOLLOWOUTDOORAIRTEMPERATURE',
    'SETPOINTMANAGER:FOLLOWSYSTEMNODETEMPERATURE',
    'SETPOINTMANAGER:MIXEDAIR',
    'SETPOINTMANAGER:MULTIZONE:COOLING:AVERAGE',
    'SETPOINTMANAGER:MULTIZONE:HEATING:AVERAGE',
    'SETPOINTMANAGER:MULTIZONE:HUMIDITY:MAXIMUM',
    'SETPOINTMANAGER:MULTIZONE:HUMIDITY:MINIMUM',
    'SETPOINTMANAGER:MULTIZONE:MAXIMUMHUMIDITY:AVERAGE',
    'SETPOINTMANAGER:MULTIZONE:MINIMUMHUMIDITY:AVERAGE',
    'SETPOINTMANAGER:OUTDOORAIRPRETREAT',
    'SETPOINTMANAGER:OUTDOORAIRRESET',
    'SETPOINTMANAGER:RETURNAIRBYPASSFLOW',
    'SETPOINTMANAGER:RETURNTEMPERATURE:CHILLEDWATER',
    'SETPOINTMANAGER:RETURNTEMPERATURE:HOTWATER',
    'SETPOINTMANAGER:SCHEDULED',
    'SETPOINTMANAGER:SCHEDULED:DUALSETPOINT',
    'SETPOINTMANAGER:SINGLEZONE:COOLING',
    'SETPOINTMANAGER:SINGLEZONE:HEATING',
    'SETPOINTMANAGER:SINGLEZONE:HUMIDITY:MAXIMUM',
    'SETPOINTMANAGER:SINGLEZONE:HUMIDITY:MINIMUM',
    'SETPOINTMANAGER:SINGLEZONE:ONESTAGECOOLING',
    'SETPOINTMANAGER:SINGLEZONE:ONESTAGEHEATING',
    'SETPOINTMANAGER:SINGLEZONE:REHEAT',
    'SETPOINTMANAGER:WARMEST',
    'SETPOINTMANAGER:WARMESTTEMPERATUREFLOW',
    'SHADINGPROPERTY:REFLECTANCE',
    'SHADOWCALCULATION',
    'SIMULATION DATA',
    'SIMULATIONCONTROL',
    'SITE:GROUNDDOMAIN:BASEMENT',
    'SITE:GROUNDDOMAIN:SLAB',
    'SITE:GROUNDREFLECTANCE',
    'SITE:GROUNDREFLECTANCE:SNOWMODIFIER',
    'SITE:GROUNDTEMPERATURE:BUILDINGSURFACE',
    'SITE:GROUNDTEMPERATURE:DEEP',
    'SITE:GROUNDTEMPERATURE:FCFACTORMETHOD',
    'SITE:GROUNDTEMPERATURE:SHALLOW',
    'SITE:HEIGHTVARIATION',
    'SITE:LOCATION',
    'SITE:PRECIPITATION',
    'SITE:SOLARANDVISIBLESPECTRUM',
    'SITE:WATERMAINSTEMPERATURE',
    'SITE:WEATHERSTATION',
    'SIZING:PARAMETERS',
    'SIZING:PLANT',
    'SIZING:SYSTEM',
    'SIZING:ZONE',
    'SOLARCOLLECTOR:UNGLAZEDTRANSPIRED:MULTISYSTEM',
    'STEAMEQUIPMENT',
    'SURFACECONTAMINANTSOURCEANDSINK:GENERIC:BOUNDARYLAYERDIFFUSION',
    'SURFACECONTAMINANTSOURCEANDSINK:GENERIC:DEPOSITIONVELOCITYSINK',
    'SURFACECONTAMINANTSOURCEANDSINK:GENERIC:PRESSUREDRIVEN',
    'SURFACECONTROL:MOVABLEINSULATION',
    'SURFACECONVECTIONALGORITHM:INSIDE',
    'SURFACECONVECTIONALGORITHM:INSIDE:ADAPTIVEMODELSELECTIONS',
    'SURFACECONVECTIONALGORITHM:OUTSIDE',
    'SURFACECONVECTIONALGORITHM:OUTSIDE:ADAPTIVEMODELSELECTIONS',
    'SURFACEPROPERTIES:VAPORCOEFFICIENTS',
    'SURFACEPROPERTY:CONVECTIONCOEFFICIENTS',
    'SURFACEPROPERTY:CONVECTIONCOEFFICIENTS:MULTIPLESURFACE',
    'SURFACEPROPERTY:EXPOSEDFOUNDATIONPERIMETER',
    'SURFACEPROPERTY:EXTERIORNATURALVENTEDCAVITY',
    'SURFACEPROPERTY:HEATTRANSFERALGORITHM',
    'SURFACEPROPERTY:HEATTRANSFERALGORITHM:CONSTRUCTION',
    'SURFACEPROPERTY:HEATTRANSFERALGORITHM:MULTIPLESURFACE',
    'SURFACEPROPERTY:HEATTRANSFERALGORITHM:SURFACELIST',
    'SURFACEPROPERTY:SOLARINCIDENTINSIDE',
    'TIMESTEP',
    'UTILITYCOST:CHARGE:BLOCK',
    'UTILITYCOST:CHARGE:SIMPLE',
    'UTILITYCOST:COMPUTATION',
    'UTILITYCOST:QUALIFY',
    'UTILITYCOST:RATCHET',
    'UTILITYCOST:VARIABLE',
    'VERSION',
    'WATERHEATER:SIZING',
    'WATERUSE:RAINCOLLECTOR',
    'WATERUSE:WELL',
    'WEATHERPROPERTY:SKYTEMPERATURE',
    'WINDOWPROPERTY:AIRFLOWCONTROL',
    'WINDOWPROPERTY:STORMWINDOW',
    'ZONEAIRBALANCE:OUTDOORAIR',
    'ZONEAIRCONTAMINANTBALANCE',
    'ZONEAIRHEATBALANCEALGORITHM',
    'ZONEAIRMASSFLOWCONSERVATION',
    'ZONEBASEBOARD:OUTDOORTEMPERATURECONTROLLED',
    'ZONECAPACITANCEMULTIPLIER:RESEARCHSPECIAL',
    'ZONECONTAMINANTSOURCEANDSINK:CARBONDIOXIDE',
    'ZONECONTAMINANTSOURCEANDSINK:GENERIC:CONSTANT',
    'ZONECONTAMINANTSOURCEANDSINK:GENERIC:CUTOFFMODEL',
    'ZONECONTAMINANTSOURCEANDSINK:GENERIC:DECAYSOURCE',
    'ZONECONTAMINANTSOURCEANDSINK:GENERIC:DEPOSITIONRATESINK',
    'ZONECONTROL:CONTAMINANTCONTROLLER',
    'ZONECONTROL:THERMOSTAT:OPERATIVETEMPERATURE',
    'ZONECONTROL:THERMOSTAT:TEMPERATUREANDHUMIDITY',
    'ZONECONTROL:THERMOSTAT:THERMALCOMFORT',
    'ZONECOOLTOWER:SHOWER',
    'ZONECROSSMIXING',
    'ZONEEARTHTUBE',
    'ZONEGROUP',
    'ZONEHVAC:EQUIPMENTCONNECTIONS',
    'ZONEINFILTRATION:DESIGNFLOWRATE',
    'ZONEINFILTRATION:EFFECTIVELEAKAGEAREA',
    'ZONEINFILTRATION:FLOWCOEFFICIENT',
    'ZONEMIXING',
    'ZONEPROPERTY:USERVIEWFACTORS:BYSURFACENAME',
    'ZONEREFRIGERATIONDOORMIXING',
    'ZONETHERMALCHIMNEY']


def find_non_reference_classes(idd_path):
    """
    Uses Eppy to parse the IDD and return the object classes that aren't
    used as reference.

    Args:
    -----
        * idd_path (str): path to the Energy+.idd
            eg: /Applications/EnergyPlus-8-7-0/Energy+.idd

    Returns:
    --------
        * not_reference_classes (list): a list of classnames that aren't
            referenced, IN UPPER CASE, and sorted

    Needs:
    ------
    eppy
    """

    from eppy.EPlusInterfaceFunctions import parse_idd

    x = parse_idd.extractidddata(idd_path)
    useful = x[2]
    not_reference_classes = []
    for i, idd_class in enumerate(useful):
        is_reference = False
        classname = idd_class[0]['idfobj']
        if len(idd_class) > 1:
            if 'reference' in idd_class[1].keys():
                if len(idd_class[1]['reference']) > 0:
                    is_reference = True
        if not is_reference:
            not_reference_classes.append(classname)

    return sorted([x.upper() for x in not_reference_classes])


def lint_and_tag_file(idf_path):
    """
    This will open a file, replace all special characters in the object names
    and output a new file. The linted object names will also be used to
    create ctags compatible statement stored in a returned list

    Args:
    -----
        * idf_path (str): a path to the IDF file

    Returns:
    --------
        * tags (list): a list of ctags statements

    Needs:
    -------

    import os

    """

    tags = []
    tag_s = "{tagname}\t{tagfile}\t/^{tagaddress}$"

    path, ext = os.path.splitext(idf_path)
    new_filename = "{}-out{}".format(path, ext)

    # Read the content of the original IDF file
    # Writen this way instead of open(, 'r', encoding='latin-1')
    # for Pyton 2/3 compat
    with open(idf_path, 'rb') as content_file:
        content = content_file.read().decode('latin-1')

    # This dict will be used to replace in the entire file content
    replacement_dict = {}

    # To find the class and object names
    objname_found = False
    classname_found = False

    # Loop on each line
    for line in content.splitlines():
        t = line.split('!')[0].strip()
        if len(t) > 0:
            if ';' in t:
                classname_found = False
                objname_found = False
            else:
                if not classname_found:
                    classname = t.split(',')[0].strip()
                    classname_found = True
                elif (not objname_found and
                      (classname.upper() not in NOT_REFERENCE_CLASSES)):

                    objname = t.split(',')[0].strip()
                    objname_found = True

                    escaped_objname = (objname.replace(" ", "_")
                                              .replace("(", "_")
                                              .replace(")", "_")
                                              .replace("[", "_")
                                              .replace("]", "_")
                                              .replace("{", "_")
                                              .replace("}", "_")
                                              .replace("/", "_")
                                              .replace("\\", "_")
                                              .replace("-", "_")
                                              .replace(".", "_")
                                              .replace(":", "_"))
                    if escaped_objname != "":
                        escaped_line = line.replace(objname, escaped_objname)

                        # Add to the replacement_dict if need be only
                        if objname != escaped_objname:
                            replacement_dict[objname] = escaped_objname

                        tag = tag_s.format(tagname=escaped_objname,
                                           tagfile=new_filename,
                                           tagaddress=escaped_line)
                        tags.append(tag)

    # Replace in the entire file content
    # We go from the most specific (longer) to the shorter
    # To avoid having problems where if I replace "A" by "B"
    # and then try to replace "AB" by "CC" it will not find "AB"
    for k in sorted(replacement_dict, key=len, reverse=True):
        content = content.replace(k, replacement_dict[k])

    # Write the new file
    with open(new_filename, 'wb') as write_file:
        write_file.write(content.encode('latin-1'))

    return tags


def tag_idfs(idf_path=None, recursive=True):
    """
    This creates a ctags file for the IDF (as well as new IDF linted file(s))

    Args:
    -----

        * idf_path (str, or None): if a path to an idf file is given, only
            this file will be tagged. Otherwise will do a glob of all idfs

        * recursive (boolean): Whether the glob needs to be recursive or not

    """

    if idf_path is None:
        if recursive is True:
            # Python 2 doesn't support recursive...
            if sys.version_info[0] < 3:
                # Python 2 doesn't support recursive...
                import fnmatch
                idf_paths = []
                for root, dirnames, filenames in os.walk('.'):
                    for filename in fnmatch.filter(filenames, '*.idf'):
                        idf_path = os.path.join(root, filename)
                        idf_paths.append(os.path.relpath(idf_path))
            else:
                idf_paths = gb.glob('**/*.idf', recursive=True)
        else:
            idf_paths = gb.glob('*.idf')
    else:
        if not os.path.splitext(idf_path)[1] == '.idf':
            raise ValueError("If `idf_path` is specified, "
                             "it must be a `.idf` file")
        if not os.path.isfile(idf_path):
            raise IOError("{} doesn't exists".format(idf_path))

        idf_paths = [idf_path]

    tags = []

    for idf_path in idf_paths:
        print("Processing: {}".format(idf_path))
        tags += lint_and_tag_file(idf_path)

    # Write tags file
    with open('tags', 'wb') as tag_file:
        tag_file.write('\n'.join(sorted(tags)).encode('latin-1'))

    print("Generated tags file: {}".format(os.getcwd()))
