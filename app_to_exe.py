# ______________________________________________________________________________
# Functions
import datetime
import logging
import queue
import shutil
import signal
import time
import tkinter as tk
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import sys
import os

# ______________________________________________________________________________
EPSG = {
    'ASCAT_125': {'ID': 'METOP', 'ext': '125_ssm_l2.bin', 'folder': 'ASCAT_SSM_125', 'channel': 'A1C-EPS-G'},
    'ASCAT_250': {'ID': 'METOP', 'ext': '250_ssm_l2.bin', 'folder': 'ASCAT_SSM_250', 'channel': 'A1C-EPS-G'},
    'NOAA_ATOVS': {'ID': 'NOAA19+ATOVS', 'ext': 'eps_o_l2.bin', 'folder': 'NOAA_ATOVS', 'channel': 'A1C-EPS-G'},
}

GEO3 = {
    'MSG_HRS15': {'ID': 'H-000-MSG', 'ext': '-C_', 'folder': 'MSG_HRS15', 'channel': 'A1C-GEO-3'},
}

GEO4 = {
    'MSG_AMV': {'ID': 'L-000-', 'ext': '-AMV_', 'folder': 'MSG_AMV', 'channel': 'A1C-GEO-4'},
    'MSG_ASR': {'ID': 'L-000-', 'ext': '-ASR_', 'folder': 'MSG_ASR', 'channel': 'A1C-GEO-4'},
    'MSG_CRR': {'ID': 'S_NWC_CRR_MSG', 'ext': '-VISIR_', 'folder': 'MSG_CRR', 'channel': 'A1C-GEO-4'},
    'MSG_CCT': {'ID': 'SAFNWC_', 'ext': '_CT_', 'folder': 'MSG_CCT', 'channel': 'A1C-GEO-4'},
    'MSG_CLM': {'ID': 'L-000-', 'ext': '-CLM_', 'folder': 'MSG_CLM', 'channel': 'A1C-GEO-4'},
    'MSG_CMa': {'ID': 'SAFNWC_', 'ext': '_CMa_', 'folder': 'MSG_CMa', 'channel': 'A1C-GEO-4'},
    'MSG_CRM': {'ID': 'L-000-', 'ext': '-CRM_', 'folder': 'MSG_CRM', 'channel': 'A1C-GEO-4'},
    'MSG_CSR': {'ID': 'L-000-', 'ext': '-CSR_', 'folder': 'MSG_CSR', 'channel': 'A1C-GEO-4'},
    'MSG_CTH': {'ID': 'L-000-', 'ext': '-CTH_', 'folder': 'MSG_CTH', 'channel': 'A1C-GEO-4'},
    'MSG_CTTH': {'ID': 'SAFNWC_', 'ext': '_CTTH_', 'folder': 'MSG_CTTH', 'channel': 'A1C-GEO-4'},
    'MSG_FIRC': {'ID': 'L-000-', 'ext': '-FIRC_', 'folder': 'MSG_FIRC', 'channel': 'A1C-GEO-4'},
    'MSG_FIRG': {'ID': 'L-000-', 'ext': '-FIRG_', 'folder': 'MSG_FIRG', 'channel': 'A1C-GEO-4'},
    'MSG_GII': {'ID': 'L-000-', 'ext': '-GII_', 'folder': 'MSG_GII', 'channel': 'A1C-GEO-4'},
    'MSG_RDT': {'ID': 'S_NWC', 'ext': '_RDT-', 'folder': 'MSG_RDT', 'channel': 'A1C-GEO-4'},
    'MSG_VOLC': {'ID': 'L-000-', 'ext': '-VOLC_', 'folder': 'MSG_VOLC', 'channel': 'A1C-GEO-4'},
    'MSG_VOLE': {'ID': 'L-000-', 'ext': '-VOLE_', 'folder': 'MSG_VOLE', 'channel': 'A1C-GEO-4'},
}

RDS1 = {
    'Metop_ASCAT_CW': {'ID': 'ascat', 'ext': 'ear_o_coa_kan_', 'folder': 'Metop_ASCAT_CW', 'channel': 'A1C-RDS-1'},
    'Metop_ASCAT_OSW': {'ID': 'ascat', 'ext': 'ear_o_250_', 'folder': 'Metop_ASCAT_OSW', 'channel': 'A1C-RDS-1'},
}

SAF1 = {
    'DMSP_GL': {'ID': 'S-OSI_-DMI_', 'ext': 'DMSP-GL', 'folder': 'DMSP_GL', 'channel': 'A1C-SAF-1'},
    'GL_OSI': {'ID': 'S-OSI_-NOR_', 'ext': '_EDGEn_', 'folder': 'GL_OSI', 'channel': 'A1C-SAF-1'},
    'Metop_ OAS025': {'ID': 'ascat', 'ext': '_eps_o_250', 'folder': 'Metop_ OAS025', 'channel': 'A1C-SAF-1'},
    'Metop_ OMRSIDRN': {'ID': 'S-OSI_-DMI_-MTOP-', 'ext': 'MRSIDRIFT-', 'folder': 'Metop_ OMRSIDRN',
                        'channel': 'A1C-SAF-1'},
    'Metop_MGRSST': {'ID': 'S-OSI_-FRA_-MTOP', 'ext': '-MGRSST_', 'folder': 'Metop_MGRSST', 'channel': 'A1C-SAF-1'},
    'Metop_OASWC12': {'ID': 'ascat', 'ext': 'eps_o_coa_', 'folder': 'Metop_OASWC12', 'channel': 'A1C-SAF-1'},
    'Metop_OSSTGLB': {'ID': 'S-OSI_-FRA_', 'ext': 'GLBSST_', 'folder': 'Metop_OSSTGLB', 'channel': 'A1C-SAF-1'},
    'Metop_OSSTIST3A': {'ID': 'S-OSI_', 'ext': 'OSSTIST3A', 'folder': 'Metop_OSSTIST3A', 'channel': 'A1C-SAF-1'},
    'MSG_SST': {'ID': '-GOES-', 'ext': '__SST_FIELD-', 'folder': 'MSG_SST', 'channel': 'A1C-SAF-1'},
    'MSG_SST_FIELD': {'ID': '-MSG_', 'ext': '__SST_FIELD-', 'folder': 'MSG_SST_FIELD++', 'channel': 'A1C-SAF-1'},
    'MULT_AHLDLISSI': {'ID': 'S-OSI_-NOR_', 'ext': 'MULT-AHLDLISSI', 'folder': 'MULT_AHLDLISSI',
                       'channel': 'A1C-SAF-1'},
    'MULT_AHLSST': {'ID': 'S-OSI_-NOR_', 'ext': 'MULT-AHLSST', 'folder': 'MULT_AHLSST**', 'channel': 'A1C-SAF-1'},
    'MULT_AMSR_CONC': {'ID': 'S-OSI_-DMI_', 'ext': 'AMSR-GL_', 'folder': 'MULT_AMSR_CONC', 'channel': 'A1C-SAF-1'},
    'MULT_GL': {'ID': 'S-OSI_-NOR_', 'ext': 'MULT_GL_', 'folder': 'MULT_GL', 'channel': 'A1C-SAF-1'},
    'MULT_NARSST': {'ID': 'S-OSI_-FRA_', 'ext': 'NARSST_', 'folder': 'MULT_NARSST', 'channel': 'A1C-SAF-1'},
    'MULT_OSIDRGB': {'ID': 'S-OSI_-NOR_', 'ext': 'LRSIDRIFT-', 'folder': 'MULT_OSIDRGB', 'channel': 'A1C-SAF-1'},
    'NPP_OSSTIST2B': {'ID': 'S-OSI_-NOR_', 'ext': 'OSSTIST2B-', 'folder': 'OSSTIST2B', 'channel': 'A1C-SAF-1'},
    'NPP_OSSTIST3B': {'ID': 'S-OSI_-NOR_', 'ext': 'OSSTIST3B-', 'folder': 'OSSTIST3B', 'channel': 'A1C-SAF-1'},
    'ScatSat_ OSSW025': {'ID': 'W_NL-KNMI-', 'ext': 'SCATSAT1+OSCAT_C_', 'folder': 'ScatSat_ OSSW025**',
                         'channel': 'A1C-SAF-1'},
}

SAF2 = {
    'Metop_AVHR_EDLST': {'ID': 'S-LSA_', 'ext': 'VHR_EDLST', 'folder': 'Metop_AVHR_EDLST', 'channel': 'A1C-SAF-2'},
    'Metop_AVHR_EDSC': {'ID': 'S-LSA_', 'ext': 'AVHR_EDSC_', 'folder': 'Metop_AVHR_EDSC', 'channel': 'A1C-SAF-2'},
    'MSG_ALBEDO': {'ID': 'S-LSA_', 'ext': '_ALBEDO_', 'folder': 'MSG_ALBEDO', 'channel': 'A1C-SAF-2'},
    'MSG_DSLF': {'ID': 'S-LSA_', 'ext': '_DSLF_', 'folder': 'MSG_DSLF', 'channel': 'A1C-SAF-2'},
    'MSG_DSSF': {'ID': 'S-LSA_', 'ext': '_DSSF_', 'folder': 'MSG_DSSF', 'channel': 'A1C-SAF-2'},
    'MSG_ET': {'ID': 'S-LSA_', 'ext': '_ET_', 'folder': 'MSG_ET', 'channel': 'A1C-SAF-2'},
    'MSG_FAPAR': {'ID': 'S-LSA_', 'ext': '_FAPAR_', 'folder': 'MSG_FAPAR', 'channel': 'A1C-SAF-2'},
    'MSG_FDeM': {'ID': 'S-LSA_', 'ext': '_FDeM_', 'folder': 'MSG_FDeM', 'channel': 'A1C-SAF-2'},
    'MSG_FRP-PIXEL': {'ID': 'S-LSA_', 'ext': '_FRP-PIXEL', 'folder': 'MSG_FRP-PIXEL', 'channel': 'A1C-SAF-2'},
    'MSG_FTA_FRP_GRID': {'ID': 'S-LSA_', 'ext': '_FTA-FRP-GRID_', 'folder': 'MSG_FTA_FRP_GRID', 'channel': 'A1C-SAF-2'},
    'MSG_FVC': {'ID': 'S-LSA_', 'ext': '_FVC_', 'folder': 'MSG_FVC', 'channel': 'A1C-SAF-2'},
    'MSG_LAI': {'ID': 'S-LSA_', 'ext': '_LAI_', 'folder': 'MSG_LAI', 'channel': 'A1C-SAF-2'},
    'MSG_LST': {'ID': 'S-LSA_', 'ext': '_LST_', 'folder': 'MSG_LST', 'channel': 'A1C-SAF-2'},
    'MSG_METREF': {'ID': 'S-LSA_', 'ext': '_METREF_', 'folder': 'MSG_METREF', 'channel': 'A1C-SAF-2'},
    'MSG_SC2': {'ID': 'S-LSA_', 'ext': '_SC2_', 'folder': 'MSG_SC2', 'channel': 'A1C-SAF-2'},
}

TPC1 = {
    'AQUA_ROPMAD': {'ID': 'PML_', 'ext': '_refined', 'folder': 'AQUA_ROPMAD', 'channel': 'A1C-TPC-1'},
    'MODIS_CPMAD': {'ID': 'PML_', 'ext': '_3daycomp_', 'folder': 'MODIS_CPMAD', 'channel': 'A1C-TPC-1'},
    'MODIS_OCPUCT': {'ID': 'UCT_', 'ext': '_chlora_', 'folder': 'MODIS_OCPUCT', 'channel': 'A1C-TPC-1'},
    'MULT_NRTOMAD': {'ID': 'PML_', 'ext': '_nrt_', 'folder': 'MULT_NRTOMAD', 'channel': 'A1C-TPC-1'},
    'MULT_NRTOMAD_afr': {'ID': 'PML_', 'ext': '_nrt_', 'folder': 'MULT_NRTOMAD', 'channel': 'A1C-TPC-1'},

}

TPC5 = {
    'Metop_SWI': {'ID': 'g2_BIOPAR', 'ext': '_SWI_', 'folder': 'Metop_SWI', 'channel': 'A1C-TPC-5'},
    'PROBA_V_BA': {'ID': 'c_gls_', 'ext': 'BA300_', 'folder': 'PROBA_V_BA', 'channel': 'A1C-TPC-5'},
    'NDVIA': {'ID': 'c_gls_', 'ext': 'NDVI300_', 'folder': 'NDVIA', 'channel': 'A1C-TPC-5'},
    'PROBA_V_SWB': {'ID': 'g2_BIOPAR', 'ext': '_WB_', 'folder': 'PROBA_V_SWB', 'channel': 'A1C-TPC-5'},
    'PROBA_V_VCI': {'ID': 'g2_BIOPAR', 'ext': '_VCI_', 'folder': 'PROBA_V_VCI', 'channel': 'A1C-TPC-5'},
    'PROBA_V_WB': {'ID': 'g2_BIOPAR', 'ext': '_WB_', 'folder': 'PROBA_V_SWB', 'channel': 'A1C-TPC-5'},
}

TPC6 = {
    'AQUA_CHLORA': {'ID': '.L3m', 'ext': '_DAY_CHL_chlor_a_', 'folder': 'AQUA_CHLORA', 'channel': 'A1C-TPC-6'},
    'DUST_DDD': {'ID': '_SDSWAS_', 'ext': 'DUST_DEPD-', 'folder': 'DUST_DDD', 'channel': 'A1C-TPC-6'},
    'DUST_DF': {'ID': '_SDSWAS_', 'ext': '-v2_EUMETCAST', 'folder': 'DUST_DF', 'channel': 'A1C-TPC-6'},
    'DUST_DLO': {'ID': '_SDSWAS_', 'ext': '-OD550_DUST-LOAD', 'folder': 'DUST_DLO', 'channel': 'A1C-TPC-6'},
    'DUST_DOD': {'ID': '_SDSWAS_', 'ext': '-OD550_DUST-', 'folder': 'DUST_DOD', 'channel': 'A1C-TPC-6'},
    'DUST_DSC': {'ID': '_SDSWAS_', 'ext': '-SCONC_DUST-', 'folder': 'DUST_DSC', 'channel': 'A1C-TPC-6'},
    'DUST_DSE': {'ID': '_SDSWAS_', 'ext': 'DUST_EXT_SFC-', 'folder': 'DUST_DSE', 'channel': 'A1C-TPC-6'},
    'DUST_DWD': {'ID': '_SDSWAS_', 'ext': '-DUST_DEPW-', 'folder': 'DUST_DWD', 'channel': 'A1C-TPC-6'},
    'MESA_UG_PFZ': {'ID': 'MESA-UG', 'ext': '_PFZ_', 'folder': 'MESA_UG_PFZ', 'channel': 'A1C-TPC-6'},
    'MESA_UG_SAL': {'ID': 'MESA-UG', 'ext': '_SAL_', 'folder': 'MESA_UG_SAL', 'channel': 'A1C-TPC-6'},
    'MESA_UG_SSC': {'ID': 'MESA-UG', 'ext': '_SSC_', 'folder': 'MESA_UG_SSC', 'channel': 'A1C-TPC-6'},
    'MESA_UG_SSH': {'ID': 'MESA-UG', 'ext': '_SSH_', 'folder': 'MESA_UG_SSH', 'channel': 'A1C-TPC-6'},
    'MESA_UG_SWH': {'ID': 'MESA-UG', 'ext': '_SWH_', 'folder': 'MESA_UG_SWH', 'channel': 'A1C-TPC-6'},
    'MESA-UG_SST': {'ID': 'MESA-UG', 'ext': '_SST_', 'folder': 'MESA-UG_SST', 'channel': 'A1C-TPC-6'},
    'MODIS_MOD_PAR': {'ID': '.L3m', 'ext': '_DAY_PAR_par_', 'folder': 'MODIS_MOD_PAR', 'channel': 'A1C-TPC-6'},
    'MODIS_MOD-KD-490': {'ID': '.L3m', 'ext': '_DAY_KD490_Kd_', 'folder': 'MODIS_MOD-KD-490', 'channel': 'A1C-TPC-6'},
    'MODIS_MOD_SST': {'ID': '.L3m', 'ext': '.DAY.SST.sst', 'folder': 'MODIS_MOD_SST', 'channel': 'A1C-TPC-6'},
    'MSG_RFE': {'ID': 'rfe', 'ext': '_', 'folder': 'MSG_RFE', 'channel': 'A1C-TPC-6'},
    'UMDL1T': {'ID': 'LC08_', 'ext': 'L1TP_', 'folder': 'UMDL1T', 'channel': 'A1C-TPC-6'},
    'WW3NAO': {'ID': 'dmn', 'ext': 'dmn_ww3_', 'folder': 'WW3NAO', 'channel': 'A1C-TPC-6'},

}
TPG1 = {
    'FY2G_AMV': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_AMV_', 'folder': 'FY2G_AMV', 'channel': 'A1C-TPG-1'},
    'FY2G_CLT': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_CLT_MLT_', 'folder': 'FY2G_CLT', 'channel': 'A1C-TPG-1'},
    'FY2G_CTA': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_CTA_MLT_', 'folder': 'FY2G_CTA', 'channel': 'A1C-TPG-1'},
    'FY2G_HPF': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_HPF_MLT_', 'folder': 'FY2G_HPF', 'channel': 'A1C-TPG-1'},
    'FY2G_OLR': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_OLR_MLT_', 'folder': 'FY2G_OLR', 'channel': 'A1C-TPG-1'},
    'FY2G_PRE': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_PRE_', 'folder': 'FY2G_PRE', 'channel': 'A1C-TPG-1'},
    'FY2G_SSI': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_SSI_VIS_', 'folder': 'FY2G_SSI', 'channel': 'A1C-TPG-1'},
    'FY2G_TBB': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_TBB_IR1_', 'folder': 'FY2G_TBB', 'channel': 'A1C-TPG-1'},
    'FY2G_TPW': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_TPW_MLT_', 'folder': 'FY2G_TPW', 'channel': 'A1C-TPG-1'},
    'FY2G_TSG': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_TSG_MLT_', 'folder': 'FY2G_TSG', 'channel': 'A1C-TPG-1'},
    'FY2G-FDI': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2G_FDI_', 'folder': 'FY2G-FDI', 'channel': 'A1C-TPG-1'},
    'FY2H_AMV': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_AMV_', 'folder': 'FY2H_AMV', 'channel': 'A1C-TPG-1'},
    'FY2H_CLT': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_CLT_MLT_', 'folder': 'FY2H_CLT', 'channel': 'A1C-TPG-1'},
    'FY2H_CTA': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_CTA_MLT_', 'folder': 'FY2H_CTA', 'channel': 'A1C-TPG-1'},
    'FY2H_HPF': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_HPF_MLT_', 'folder': 'FY2H_HPF', 'channel': 'A1C-TPG-1'},
    'FY2H_OLR': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_OLR_MLT_', 'folder': 'FY2H_OLR', 'channel': 'A1C-TPG-1'},
    'FY2H_PRE': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_PRE_', 'folder': 'FY2H_PRE', 'channel': 'A1C-TPG-1'},
    'FY2H_SSI': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_SSI_VIS_', 'folder': 'FY2H_SSI', 'channel': 'A1C-TPG-1'},
    'FY2H_TBB': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_TBB_IR1_', 'folder': 'FY2H_TBB', 'channel': 'A1C-TPG-1'},
    'FY2H_TPW': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_TPW_MLT_', 'folder': 'FY2H_TPW', 'channel': 'A1C-TPG-1'},
    'FY2H_TSG': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_TSG_MLT_', 'folder': 'FY2H_TSG', 'channel': 'A1C-TPG-1'},
    'FY2H-FDI': {'ID': 'Z_SATE_C_BABJ_', 'ext': '_O_FY2H_FDI_', 'folder': 'FY2H-FDI', 'channel': 'A1C-TPG-1'},
    'INSAT3D_GPI': {'ID': '3DIMG_', 'ext': '_L2G_GPI', 'folder': 'INSAT3D_GPI', 'channel': 'A1C-TPG-1'},
    'INSAT3D_HEM': {'ID': '3DIMG_', 'ext': '_L2B_HEM', 'folder': 'INSAT3D_HEM', 'channel': 'A1C-TPG-1'},
    'INSAT3D_IMR': {'ID': '3DIMG_', 'ext': '_L2G_IMR', 'folder': 'INSAT3D_IMR', 'channel': 'A1C-TPG-1'},
    'INSAT3D_IRW': {'ID': '3DIMG_', 'ext': '_L2P_', 'folder': 'INSAT3D_IRW', 'channel': 'A1C-TPG-1'},
    'INSAT3D_OLR': {'ID': '3DIMG_', 'ext': '_L2B_OLR', 'folder': 'INSAT3D_OLR', 'channel': 'A1C-TPG-1'},
    'INSAT3D_SND': {'ID': '3DSND_', 'ext': '_L2B_SA', 'folder': 'INSAT3D_SND', 'channel': 'A1C-TPG-1'},
    'INSAT3D_SST': {'ID': '3DIMG_', 'ext': '_L2B_SST', 'folder': 'INSAT3D_SST', 'channel': 'A1C-TPG-1'},
    'INSAT3D_UTH': {'ID': '3DIMG_', 'ext': '_L2B_UTH', 'folder': 'INSAT3D_UTH', 'channel': 'A1C-TPG-1'},
    'INSAT3D_WVW': {'ID': '3DIMG_', 'ext': '_L2P_WVW', 'folder': 'INSAT3D_WVW', 'channel': 'A1C-TPG-1'},

}
# ______________________________________________________________________________
# Info Text

info_epsg = """
																		Available Data Products in A1C-EPS-G Channel: 3 Products    

#########################################################################################################################################################################
							1. ASCAT SOIL MOISTURE AT 12.5 KM SWATH GRID IN NRT - METOP
#########################################################################################################################################################################
DESCRIPTION: The Soil Moisture (SM) product is derived from the Advanced SCATterometer (ASCAT) backscatter observations and given in swath orbit geometry 
(25 km sampling). This SM product provides an estimate of the water content of the 0-5 cm topsoil layer, expressed in degree of saturation between 0 and 100 [%]. 
The algorithm used to derive this parameter is based on a linear relationship of SM and scatterometer backscatter and uses change detection techniques to eliminate 
the contributions of vegetation, land cover and surface topography, considered invariant from year to year. Seasonal vegetation effects are modelled by exploiting 
the multi-angle viewing capabilities of ASCAT. The SM processor has been developed by Vienna University of Technology (TU Wien). Note that some of the data are 
reprocessed. Please refer to the associated product validation reports or product release notes for further information.
STORAGE FOLDER: ASCAT_SSM_125


#########################################################################################################################################################################
							2. ASCAT SOIL MOISTURE AT 25 KM SWATH GRID IN NRT - METOP
#########################################################################################################################################################################
DESCRIPTION: The Soil Moisture (SM) product is derived from the Advanced SCATterometer (ASCAT) backscatter observations and given in swath orbit geometry
(25 km sampling).This SM product provides an estimate of the water content of the 0-5 cm topsoil layer, expressed in degree of saturation between 0 and 100 [%]. 
The algorithm used to derive this parameter is based on a linear relationship of SM and scatterometer backscatter and uses change detection techniques to eliminate 
the contributions of vegetation, land cover and surface topography, considered invariant from year to year. Seasonal vegetation effects are modelled by exploiting 
the multi-angle viewing capabilities of ASCAT. The SM processor has been developed by Vienna University of Technology (TU Wien). Note that some of the data are 
reprocessed. Please refer to the associated product validation reports or product release notes for further information.
STORAGE FOLDER: ASCAT_SSM_250

#########################################################################################################################################################################
									3. ATOVS SOUNDING PRODUCTS - NOAA
#########################################################################################################################################################################
DESCRIPTION: The Advanced TIROS Operational Sounder (ATOVS), in combination with the Advanced Very High-Resolution Radiometer (AVHRR), covers the visible, infrared and 
microwave spectral regions and thus has a wide range of applications: supplementing the retrieval of vertical temperature and humidity profiles, cloud and precipitation 
monitoring, sea ice and snow cover detection as well as surface temperature determination. ATOVS is composed of the Advanced Microwave Sounding Unit A, the Microwave 
Humidity Sounder (MHS) and the High-Resolution Infrared Radiation Sounder (HIRS/4).
STORAGE FOLDER: NOAA_ATOVS

"""

info_geo3 = """
																		Available Data Products in A1C-GEO-3 Channel    

#########################################################################################################################################################################
								1. HIGH RATE SEVIRI LEVEL 1.5 IMAGE DATA – MSG
#########################################################################################################################################################################
DESCRIPTION: Rectified (level1.5) Meteosat SEVIRI image data. The data is transmitted as High-Rate transmissions in 12 spectral channels. Level 1.5 image data 
corresponds to the geolocated and radiometrically pre-processed image data, ready for further processing, e.g., the extraction of meteorological products. Any 
spacecraft specific effects have been removed, and in particular, linearisation and equalisation of the image radiometry has been performed for all SEVIRI channels. 
The on-board blackbody data has been processed. Both radiometric and geometric quality control information is included. Images are made available with different 
timeliness according to the latency: quarter-hourly images with a latency of more than 3 hours and hourly images if latency is less than 3 hours (for a total of 
87 images per day). To enhance the perception for areas which are on the night side of the Earth a different mapping with increased contrast is applied for IR3.9 
product. The greyscale mapping is based on the EBBT which allows to map the ranges 200 K to 300 K for the night and 250 K to 330 K for the day.
STORAGE FOLDER: MSG_HRS15

"""

info_geo4 = """
																		Available Data Products in A1C-GEO-4 Channel: 16 Products    
#########################################################################################################################################################################
								1. ATMOSPHERIC MOTION VECTORS - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: Atmospheric Motion Vectors at all heights below the tropopause, derived from 5 channels (Visual 0.8, Water Vapor 6.2, Water Vapor 7.3, Infrared 10.8 and 
the High-Resolution Visual channel), all combined into one product. Vectors are derived by tracking the motion of clouds and other atmospheric constituents as water 
vapor patterns. The initial resolution is a 24 pixels grid (HRV 12 high res. pixels), but as the algorithm tries to adjust the position to the point of the maximum 
contrast (typically cloud edges), the end resolution varies. The height assignment of the AMVs is calculated using the Cross-Correlation Contribution (CCC) function 
to determine the pixels that contribute the most to the vectors. An AMV product contains between 30 000 and 50 000 vectors depending of the time of the day, and uses 
SEVERI image data from Meteosat-8 and onwards
STORAGE FOLDER: MSG_AMV

#########################################################################################################################################################################
								2. ALL-SKY RADIANCE – MSG – 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: The All-Sky Radiances (ASR) product contains information on mean brightness temperatures from all thermal (e.g., infrared and water vapor) channels. It 
includes both clear and cloudy sky brightness temperatures. Applications and Users: Numerical weather prediction.
STORAGE FOLDER: MSG_ASR

#########################################################################################################################################################################
								3. CONVECTIVE RAIN RATE - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: The Convective Rain Rate product is a geostationary meteorological product for nowcasting applications. It is produced with NWC-SAF Geo 2016 software 
package.
STORAGE FOLDER: MSG_CRR

#########################################################################################################################################################################
								4. GEOSTATIONARY NOWCASTING CLOUD TYPE - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: Cloud classification produced with NWC-SAF Geo software package, PGE02.
STORAGE FOLDER: MSG_CCT

#########################################################################################################################################################################
								5. CLOUD MASK - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: The Cloud Mask product describes the scene type (either 'clear' or 'cloudy') on a pixel level. Each pixel is classified as one of the following four types: 
clear sky over water, clear sky over land, cloud, or not processed (off Earth disc). Applications & Uses: The main use is in support of Nowcasting applications, 
where it frequently serves as a basis for other cloud products, and the remote sensing of continental and ocean surfaces.
STORAGE FOLDER: MSG_CLM

#########################################################################################################################################################################
								6. GEOSTATIONARY NOWCASTING CLOUD MASK - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: Cloud mask including dust flag and volcanic ash flag produced with NWC-SAF Geo software package.
STORAGE FOLDER: MSG_CMa

#########################################################################################################################################################################
								7. CLEAR SKY REFLECTANCE MAP - MSG – 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: Reflectances from the four MSG solar channels. Seven-day average of cloud-free pixels in the 12:00 UTC images. Applications and Users: Used to perform cloud 
masking with visible channels. Also, information source for climate and land surface applications. The product is available on request only. In addition to the daily 
12:00 UTC images, the Data Centre offers also some products generated at different times of day. These 6 additional products are provided once a week (Wednesdays) in 
the time range between 06:00 and 18:00 UTC.
STORAGE FOLDER: MSG_CRM

#########################################################################################################################################################################
								8. CLEAR SKY RADIANCES - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: The Clear-Sky Radiances (CSR) product is a subset of the information derived during the Scenes Analysis processing. The product provides the brightness 
temperature for a subset of the MSG channels averaged over all pixels within a processing segment which have been identified as clear, except for channel WV6.2 
where the CSR is also derived for areas containing low-level clouds. The final CSR product is BUFR encoded at every third quarter of the hour (e.g., 00:45, 01:45 ...) 
and distributed to the users via EUMETCAST and GTS. It is also stored in the EUMETSAT Data Centre. Applications and Users: Numerical weather prediction.
STORAGE FOLDER: MSG_CSR

#########################################################################################################################################################################
								9. CLOUD TOP HEIGHT - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: The product indicates the height of highest cloud. Based on a subset of the information derived during Scenes and Cloud Analysis, but also makes use of 
other external meteorological data. Applications and Users: Aviation meteorology.
STORAGE FOLDER: MSG_CTH

#########################################################################################################################################################################
								10. GEOSTATIONARY NOWCASTING CLOUD TOP TEMPERATURE AND HEIGHT - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: Cloud mask including dust flag and volcanic ash flag produced with NWC-SAF Geo software package.
STORAGE FOLDER: MSG_CTTH

#########################################################################################################################################################################
								11. ACTIVE FIRE MONITORING (CAP) - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: The active fire monitoring product is a fire detection product indicating the presence of fire within a pixel. The underlying concept of the algorithm 
takes advantage of the fact that SEVIRI channel IR3.9 is very sensitive to hot spots which are caused by fires. The algorithm distinguishes between potential fire 
and active fire. Applications and Users: Fire detection and monitoring. This product is available in CAP (Common Alert Protocol) format. The CAP formatted product 
is only disseminated when a fire/potential fire is detected in any given repeat cycle.
STORAGE FOLDER: MSG_FIRC

#########################################################################################################################################################################
								12. ACTIVE FIRE MONITORING (GRIB) - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: The active fire monitoring product is a fire detection product indicating the presence of fire within a pixel. The underlying concept of the algorithm 
takes advantage of the fact that SEVIRI channel IR3.9 is very sensitive to hot spots which are caused by fires. The algorithm distinguishes between potential fire and 
active fire. Applications and Users: Fire detection and monitoring.
STORAGE FOLDER: MSG_FIRG

#########################################################################################################################################################################
								13. GLOBAL INSTABILITY INDEX - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: Atmospheric air mass instability in cloud free areas. The product contains several stability parameters as well as information about the precipitable water
contents of the atmosphere. For more information on the parameters and algorithms refer to the product guide in the resources. The algorithm is a physical retrieval 
scheme developed at EUMETSAT. Applications and Users: Nowcasting and short-term forecasting (up to 12 hours). Resolution is 3x3 pixels.
STORAGE FOLDER: MSG_GII

#########################################################################################################################################################################
								14. RAPIDLY DEVELOPING THUNDERSTORMS - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: Rapidly Developing Thunderstorms - Convection Warning product is a geostationary meteorological product for nowcasting applications. It is produced with 
the NWC-SAF Geo 2016 software package.
STORAGE FOLDER: MSG_RDT

#########################################################################################################################################################################
								15. VOLCANIC ASH DETECTION (CAP) - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: The ash detection is based on a reversed split window technique, supported by tests in the other IR channels and two VIS channels. The CAP formatted product
 provides an area defined by a polygon containing the ash mass loading as main parameter. The generation and dissemination shall only be activated after the reception 
of an alert from the VAAC-London. Applications & Users: Support to ash monitoring, aviation. Current users are the Volcanic Ash Advisory Centre and Member States 
National Meteorological Services (NMS). Used input data include: the reflectances in the VIS0.6 and the IR3.9 channels; the brightness temperatures in the IR3.9, 
IR8.7, IR10.8 and IR12:0 channels and the solar zenith angle on pixel level.
STORAGE FOLDER: MSG_VOLC

#########################################################################################################################################################################
								16. VOLCANIC ASH DETECTION (NETCDF) - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: The ash detection is based on a reversed split window technique, supported by tests in the other IR channels and two VIS channels. The product is 
disseminated in netCDF classic format, that contains as main parameters the ash mass loading and the mean ash particle size. Note that the netCDF 
files have been compressed with bzip2 and before uncompressing them, the 103 bytes LRIT header must first be removed After decompression, any reader 
compatible with netCDF classic format (also known as netCDF-3), written with netCDF library version 4.1.1, can be used to read the data. The 
navigation data is not supplied within the netCDF product but can be found in the online resources
STORAGE FOLDER: MSG_VOLE

"""

info_rds1 = """
																		Available Data Products in A1C-RDS-1 Channel: 2 Products    
#########################################################################################################################################################################
								1. ASCAT COASTAL WINDS AT 12.5 KM - METOP - REGIONAL DATA SERVICE
#########################################################################################################################################################################
DESCRIPTION: Equivalent neutral 10m winds over the global oceans, with specific sampling to provide as many observations as possible near the coasts. The data is 
acquired from the EUMETSAT Advanced Retransmission Service (EARS) network of Direct Readout stations. Additionally, from Metop-A the last 30 minutes of ASCAT data in 
the main Svalbard data dump are processed. All data are processed jointly by the EARS ground system and the Koningklijk Nederland’s Meteorologisch Instituut (KNMI) 
within 45 minutes. This product is intended for assimilation in Regional Numerical Weather prediction models, where high timeliness is very important in order to 
address the short model cut-off times.
STORAGE FOLDER: Metop_ASCAT_CW

#########################################################################################################################################################################
								2. ASCAT OCEAN SURFACE WINDS AT 25 KM NODE GRID - METOP - REGIONAL DATA SERVICE
#########################################################################################################################################################################
DESCRIPTION: The ASCAT Wind Product contains measurements of the wind direction and wind speed at 10 m above the sea surface. The measurements are obtained through 
the processing of scatterometer data originating from the ASCAT instrument on EUMETSAT's Metop satellite, as described in the ASCAT Wind Product User Manual. In the 
context of this regional service, the data is acquired both from the last 30 minutes of the ASCAT. Metop main Svalbard dump, as well as from the EUMETSAT Advanced 
Retransmission Service (EARS) network of Direct Readout stations in Europe and the middle East. All data are processed jointly by the EARS ground system and the 
Koningklijk Nederlands Meteorologisch Instituut (KNMI) within 45 minutes. This product is intended for assimilation in Regional Numerical Weather prediction models, 
where high timeliness is very important in order to address the short model cut-off times.
STORAGE FOLDER: Metop_ASCAT_OSW

"""

info_saf1 = """
																		Available Data Products in A1C-SAF-1 Channel: 19 Products    
#########################################################################################################################################################################
								1. GLOBAL SEA ICE EMISSIVITY - DMSP
#########################################################################################################################################################################
DESCRIPTION: The microwave sea ice surface emissivity for solving the radiative transfer equation for top of the atmosphere up-welling Earth emission.
STORAGE FOLDER: DMSP_GL

#########################################################################################################################################################################
								2. GLOBAL SEA ICE EDGE (NETCDF) –MULTIMISSION
#########################################################################################################################################################################
DESCRIPTION: This product consists in Metop/AVHRR full resolution (1 km at nadir) sub-skin Sea Surface Temperature granules. Granules are disseminated every 3 minutes 
through EUMETCast. The product format is compliant with the Data Specification (GDS) version 2 from the Group for High Resolution Sea Surface Temperatures (GHRSST).
STORAGE FOLDER: GL_OSI

#########################################################################################################################################################################
								3. ASCAT WINDS AND SOIL MOISTURE AT 25 KM SWATH GRID - METOP
#########################################################################################################################################################################
DESCRIPTION: This ASCAT Multi-parameter product contains surface wind vectors over ocean and soil moisture index over land. Additionally, the backscatter values 
involved in the retrieval of the geophysical parameters above are also included, as well as several quality flags to facilitate the use of the data. For NWP users this 
product is provided in BUFR format. The netCDF version of this product contains Winds ONLY. For users interested in either ASCAT backscatter, wind or soil moisture 
index data in other formats, please refer to the relevant product entries available for the specific parameters. Finally, note that although the OSI SAF is identified 
as the originating centre for this product, it is not responsible for the processing of soil moisture index values, which is currently carried out at EUMETSAT. Better 
than using this archived NRT product, please use the reprocessed ASCAT winds data records (EO:EUM:DAT:METOP:OSI-150-A, EO:EUM:DAT:METOP:OSI-150-B).
STORAGE FOLDER: Metop_ OAS025

#########################################################################################################################################################################
								4. MEDIUM RESOLUTION SEA ICE DRIFT - METOP
#########################################################################################################################################################################
DESCRIPTION: Medium Resolution Sea Ice Drift product covers The Northern Hemisphere (NH) above 40 Deg. N. Ice motion vectors with a time span of approximately 24 hours 
are estimated by a maximum cross-correlation method (MCC) on pairs of satellite images. The ice drift product is based on swath data from the AVHRR instrument onboard 
the Metop-A satellite. VISible data are used to determine ice motion during summer (MJJA). and Thermal InfraRed data are used from September to April. Valid drift data 
are only available in cloud free areas, due to cloud opacity of VIS and TIR data.
STORAGE FOLDER: Metop_ OMRSIDRN

#########################################################################################################################################################################
								5. FULL RESOLUTION L2P AVHRR SEA SURFACE TEMPERATURE METAGRANULES (GHRSST) - METOP
#########################################################################################################################################################################
DESCRIPTION: This product consists in Metop/AVHRR full resolution (1 km at nadir) sub-skin Sea Surface Temperature granules. Granules are disseminated every 3 minutes 
through EUMETCast. The product format is compliant with the Data Specification (GDS) version 2 from the Group for High Resolution Sea Surface Temperatures (GHRSST).
STORAGE FOLDER: Metop_MGRSST

#########################################################################################################################################################################
								6. ASCAT COASTAL WINDS AT 12.5 KM SWATH GRID - METOP
#########################################################################################################################################################################
DESCRIPTION: Equivalent neutral 10m winds over the global oceans, with specific sampling to provide as many observations as possible near the coasts. Better than using 
this archived NRT product, please use the reprocessed ASCAT winds data records (EO:EUM:DAT:METOP:OSI-150-A, EO:EUM:DAT:METOP:OSI-150-B).
STORAGE FOLDER: Metop_OASWC12

#########################################################################################################################################################################
								7. GLOBAL L3C AVHRR SEA SURFACE TEMPERATURE (GHRSST) - METOP
#########################################################################################################################################################################
DESCRIPTION: Global Metop/AVHRR sub-skin Sea Surface Temperature (GBL SST) is a 12-hourly synthesis on a 0.05° global grid. The product format is compliant with the 
Data Specification (GDS) version 2 from the Group for High Resolution Sea Surface Temperatures (GHRSST).
STORAGE FOLDER: Metop_OSSTGLB

#########################################################################################################################################################################
								8. NORTHERN HIGH LATITUDE L3 SEA AND SEA ICE SURFACE TEMPERATURE - METOP-B
#########################################################################################################################################################################
DESCRIPTION: NRT 12 hourly aggregated SST and IST product for northern high latitudes (poleward of 50N). It is based on AVHRR data.
STORAGE FOLDER: Metop_OSSTIST3A

#########################################################################################################################################################################
								9. L3C HOURLY SEA SURFACE TEMPERATURE (GHRSST) – MSG
#########################################################################################################################################################################
DESCRIPTION: Hourly sub-skin Sea Surface Temperature product derived from Meteosat at 0° longitude, covering 60S-60N and 60W-60E and re-projected on a 0.05° regular 
grid. The product format is compliant with the Data Specification (GDS) version 2 from the Group for High Resolution Sea Surface Temperatures (GHRSST). This 
Meteosat-11 based product is available only from 20/02/2018. For data before this date, we advise you to use the2004-2012: L3C hourly Sea Surface Temperature 
(GHRSST) data record release 1 - MSG which is in the same GHRSST-compliant format2011-2017: L3C hourly Sea Surface Temperature (GRIB) - MSG which is in GRIB format. 
The same data but in GHRSST-compliant format can be found on the OSI SAF LML FTP server (Ifremer).
STORAGE FOLDER: MSG_SST

#########################################################################################################################################################################
								10. L3C HOURLY SEA SURFACE TEMPERATURE (GHRSST) - MSG
#########################################################################################################################################################################
DESCRIPTION: Hourly sub-skin Sea Surface Temperature product derived from Meteosat at 0° longitude, covering 60S-60N and 60W-60E and re-projected on a 0.05° regular grid. 
The product format is compliant with the Data Specification (GDS) version 2 from the Group for High Resolution Sea Surface Temperatures (GHRSST).
This Meteosat-11 based product is available only from 20/02/2018. For data before this date, we advice you to use the 2004-2012: L3C hourly Sea Surface Temperature 
(GHRSST) data record release 1 - MSG which is in the same GHRSST-compliant format 2011-2017: L3C hourly Sea Surface Temperature (GRIB) - MSG which is in GRIB format. 
The same data but in GHRSST-compliant format can be found on the OSI SAF LML FTP server (Ifremer).
STORAGE FOLDER: MSG_SST_FIELD

#########################################################################################################################################################################
								11. ATLANTIC HIGH LATITUDE SURFACE SOLAR IRRADIANCE (NETCDF) - MULTIMISSION
#########################################################################################################################################################################
DESCRIPTION: Estimation of the daily solar irradiance reaching the Earth surface, derived from AVHRR data on board the polar orbiting satellites from EUMETSAT and NOAA 
over the Atlantic High Latitudes. The daily value is the integration of all the orbital values in the UT day. The product is remapped onto a 5km polar stereographic 
grid and expressed in W/m2.
STORAGE FOLDER: MULT_AHLDLISSI

#########################################################################################################################################################################
								12. ATLANTIC HIGH LATITUDE SEA SURFACE TEMPERATURE - MULTIMISSION
#########################################################################################################################################################################
DESCRIPTION: Calculation of underskin temperature (°C) with multispectral algorithm. The product covers the Atlantic High Latitudes and is delivered twice daily on a 
5km polar stereographic grid.
STORAGE FOLDER: MULT_AHLSST

#########################################################################################################################################################################
								13. GLOBAL AMSR SEA ICE CONCENTRATION - GCOM-W1
#########################################################################################################################################################################
DESCRIPTION: The High Latitude Level 3 Global AMSR Sea Ice Concentration consists of these major fields: Sea ice concentration - Indicates the fraction of a given ocean 
grid point covered by ice. Uncertainties - The algorithm uncertainty, the smearing uncertainty and the resulting total uncertainty of each sea ice concentration grid 
cell. Confidence level - Based on the daily standard deviation within each grid cell, provided as a guide. This product is complementary to the SSMIS global sea ice 
concentration product (OSI-401-b).
STORAGE FOLDER: MULT_AMSR_CONC

#########################################################################################################################################################################
								14. GLOBAL SEA ICE TYPE (NETCDF) - MULTIMISSION
#########################################################################################################################################################################
DESCRIPTION: The Sea Ice Type product is a classification product (multiyear ice/first-year ice) and covers both the Northern Hemisphere (NH) and Southern Hemisphere 
(SH). The sea ice type is derived from passive microwave and active microwave sensors using a multi sensor methods with a Bayesian approach to combine the different 
sensors. At present, it is not possible to do an ice type classification during summer from the processed channels. Accordingly, the NH ice type product files 
distributed between mid-May and 30 September do not contain any valid classification. Similarly, for the SH, at present no ice type classification has been defined and 
SH product files do not contain valid classification.
STORAGE FOLDER: MULT_GL

#########################################################################################################################################################################
								15. L3C NORTH ATLANTIC REGIONAL (NAR) SEA SURFACE TEMPERATURE (GHRSST) -MULTIMISSION
#########################################################################################################################################################################
DESCRIPTION: NAR product consists in Metop/AVHRR and SNPP/VIIRS derived sub-skin Sea Surface Temperature over North Atlantic and European Seas at 2 km resolution, four 
times a day. The product format is compliant with the Data Specification (GDS) version 2 from the Group for High Resolution Sea Surface Temperatures (GHRSST).
STORAGE FOLDER: MULT_NARSST

#########################################################################################################################################################################
								16. GLOBAL LOW RESOLUTION SEA ICE DRIFT - MULTIMISSION
#########################################################################################################################################################################
DESCRIPTION: Low Resolution Sea Ice Drift product covers both Northern Hemisphere (NH) and Southern Hemisphere (SH), all year round. Ice motion vectors with a time 
span of 48 hours are estimated by an advanced cross-correlation method (the Continuous MCC, CMCC) from pairs of passive and active microwave satellite images. Several 
single-sensor products are available, as well as a merged (multi-sensor) product. Maps of uncertainties are embedded in the product files. Due to higher atmospheric 
wetness and sea ice surface melting, it is more challenging to track ice motion during summer. Accordingly, the NH product files distributed between 1 May and 30 
September have larger uncertainties and more interpolated vectors. The same holds for the SH product files between 1 November and 30 March.
STORAGE FOLDER: MULT_OSIDRGB

#########################################################################################################################################################################
								17. HIGH LATITUDE L2 SEA AND SEA ICE SURFACE TEMPERATURE - NPP
#########################################################################################################################################################################
DESCRIPTION: Integrated high latitude Surface Temperature product. The product covers the sea and ice areas polewards of latitudes 50N.
STORAGE FOLDER: NPP_OSSTIST2B

#########################################################################################################################################################################
								18. NORTHERN HIGH LATITUDE L3 SEA AND SEA ICE SURFACE TEMPERATURE - NPP
#########################################################################################################################################################################
DESCRIPTION: NRT 12 hourly aggregated SST and IST product for northern high latitudes (poleward of 50N). It is based on NPP VIIRS data.
STORAGE FOLDER: NPP_OSSTIST3B

#########################################################################################################################################################################
								19. OSCAT WINDS AT 25 KM SWATH GRID - SCATSAT
#########################################################################################################################################################################
DESCRIPTION: Stress-equivalent 10m winds over the global oceans obtained from the ScatSat-1 OSCAT scatterometer.
STORAGE FOLDER: ScatSat_ OSSW025

"""

info_saf2 = """
																		Available Data Products in A1C-SAF-2 Channel: 15 Products    

#########################################################################################################################################################################
								1. DAILY LAND SURFACE TEMPERATURE – METOP
#########################################################################################################################################################################
DESCRIPTION: Land Surface Temperature (LST) is the radiative skin temperature over land. The EDLST (EPS Daily Land Surface Temperature) provides a day-time and nigh-
time retrievals of LST based on clear-sky measurements from the Advanced Very High-Resolution Radiometer (AVHRR) on-board EUMETSAT polar system satellites, the Metop 
series.
STORAGE FOLDER: Metop_AVHR_EDLST

#########################################################################################################################################################################
								2. DAILY SNOW COVER – METOP
#########################################################################################################################################################################
DESCRIPTION: Snow Cover (SC) is the presence of snow over land. SC plays an important role in the physics of land surface as it is involved in the processes of energy 
and water exchange with the atmosphere. SC is useful for the scientific community, namely for those dealing with meteorological and climate models. Accurate detection 
of snow in a pixel is also important for a wide range of areas related to land surface processes, including meteorology, hydrology, climatology and environmental 
studies. This product is generated by the LSA SAF on behalf of the H SAF
STORAGE FOLDER: Metop_AVHR_EDSC

#########################################################################################################################################################################
								3. SURFACE ALBEDO – MSG
#########################################################################################################################################################################
DESCRIPTION: Land surface albedo is a key variable for characterizing the energy balance in the coupled soil vegetation- atmosphere system. The albedo quantifies the 
part of the energy that is absorbed and transformed into heat and latent fluxes. Owing to strong feedback effects the knowledge of albedo is important
for determining weather conditions at the atmospheric boundary layer. Climate sensitivity studies with Global Circulation Models have confirmed the 
unsteady nature of the energy balance with respect to small changes in surface albedo. Other domains of applications are in hydro-meteorology, 
agro-meteorology and environment-related studies. Two products are pre-operational, the first is available daily and the second is a 10-day composite 
(See distribution for details).
STORAGE FOLDER: MSG_ALBEDO

#########################################################################################################################################################################
								4. DOWNWELLING SURFACE LW FLUXES – MSG
#########################################################################################################################################################################
DESCRIPTION: Downwelling Surface Longwave Radiation Flux (DSLF) is the result of atmospheric absorption, emission and scattering within the entire atmospheric column 
and may be defined as the thermal irradiance reaching the surface in the thermal infrared spectrum (4-100mm). In clear sky situations DSLF depends on the vertical 
profiles of temperature and gaseous absorbers (primarily the water-vapour followed by CO2, and others of smaller importance like O3, CH4, N2O and CFCs). DSLF is 
directly related to the greenhouse effect and its monitoring has an important role in climate change studies. Other applications include meteorology (land applications)
and oceanography (air-sea-ice interaction studies). Two products are operationally available, the first is available every 30 minutes and the second is a composite 
daily product (See distribution for details)..
STORAGE FOLDER: MSG_DSLF

#########################################################################################################################################################################
								5. DOWNWELLING SURFACE SW FLUXES – MSG
#########################################################################################################################################################################
DESCRIPTION: The down-welling surface short-wave radiation flux (DSSF) refers to the radiative energy in the wavelength interval [0.3 microns, 4.0 microns] reaching the
Earth's surface per time and surface unit. It essentially depends on the solar zenith angle, on cloud coverage, and to a lesser extent on atmospheric absorption and 
surface albedo. DSSF fields are crucial for a wide number of applications involving scientific domains like weather forecast, hydrology, climate, agriculture and 
environment-related studies. In numerical weather prediction and general circulation models of the atmosphere, satellite derived DSSF estimates can either be used as a 
control variable or as a substitute to surface radiation measurement networks. Two products are operationally available, the first is available every 30 minutes and the 
second is a composite daily product (See distribution for details).
STORAGE FOLDER: MSG_DSSF

#########################################################################################################################################################################
								6. EVAPOTRANSPIRATION V2 - MSG - 0 DEGREE
#########################################################################################################################################################################
DESCRIPTION: Evapotranspiration (ET) accounts for the flux of water evaporated at the Earth-atmosphere interface (from soil, water bodies and interception) and 
transpired by vegetation through stomata in its leaves as a consequence of photosynthetic processes.
STORAGE FOLDER: MSG_ET

#########################################################################################################################################################################
								7. DAILY FRACTION OF ABSORBED PHOTOSYNTHETIC ACTIVE RADIATION – MSG
#########################################################################################################################################################################
DESCRIPTION: Fraction of Absorbed Photosynthetically Active Radiation (FAPAR) defines the fraction of PAR (400-700 nm) absorbed by the green parts of the canopy, and 
thus expresses the canopy's energy absorption capacity. FAPAR depends both on canopy structure, leaf and soil optical properties and irradiance conditions. FAPAR has 
been recognized as one of the fundamental terrestrial state variables in the context of the global change sciences (Steering Committee for GCOS, 2003; Gobron et al., 
2006). It is a key variable in models assessing vegetation primary productivity and, more generally, in carbon cycle models implementing up-to-date land surfaces 
process schemes. Besides, FAPAR it is an indicator of the health of vegetation. FAPAR is generally well correlated with the LAI, the more for healthy fully developed 
vegetation canopies. These data formats are available via this distribution method.
STORAGE FOLDER: MSG_FAPAR

#########################################################################################################################################################################
								8. FIRE DETECTION AND MONITORING – MSG
#########################################################################################################################################################################
DESCRIPTION: FD&M is based on the algorithm FIDALGO (Fire Detection Algorithm) developed within the LSA SAF (Amraoui et al., 2010) to identify SEVIRI/Meteosat pixels 
potentially contaminated by fires.
STORAGE FOLDER: MSG_FDeM

#########################################################################################################################################################################
								9. FIRE RADIATIVE POWER PIXEL – MSG
#########################################################################################################################################################################
DESCRIPTION: The Fire Radiative Power product (FRP, in megawatts) provides information on the measured radiant heat output of detected fires. It has been demonstrated 
in small-scale experimental fires that the amount of radiant heat energy liberated per unit time (the Fire Radiative Power) is related to the rate at which fuel is 
being consumed. This is a direct result of the combustion process; whereby carbon-based fuel is oxidized to CO2 with the release of a certain heat yield. Therefore, 
measuring this FRP and integrating it over the lifetime of the fire provides an estimate of the total Fire Radiative Energy (FRE), which for wildfires should be 
proportional to the total mass of fuel biomass combusted. Geostationary observations allow high temporal frequency FRP measurements, and thus a much-improved ability 
to estimate FRE via temporal integration when compared to the far less-frequent observations made from systems in low-Earth orbit. The FRP product is derived every 15 
min at the native SEVIRI pixel resolution. The disseminated product includes for each processed pixel, the FRP (MW), the corresponding uncertainty in the FRP retrieval 
based on the variability of the background radiance estimation, and a confidence measure (representing the level of confidence that the observation is indeed a true 
fire). Applications: The FRP product is intended to support emerging operational atmosphere and climate-related applications, such as Air quality forecasting, Carbon 
cycle assessment and modelling, and Fire activity models.
STORAGE FOLDER: MSG_FRP_GRID


#########################################################################################################################################################################
								10. FIRE RADIATIVE POWER GRID – MSG
#########################################################################################################################################################################
DESCRIPTION: The FRPGRID product contains an hourly estimation of the FRP at one-degree resolution and includes several correction factors. The Fire Radiative Power 
product (FRP, in MWatts) provides information on the measured radiant heat output of detected fires. It has been demonstrated in small-scale experimental fires that the 
amount of radiant heat energy liberated per unit time (the Fire Radiative Power) is related to the rate at which fuel is being consumed [1]. This is a direct result of 
the combustion process; whereby carbon-based fuel is oxidized to CO2 with the release of a certain 'heat yield'. Therefore, measuring this FRP and integrating it over 
the lifetime of the fire provides an estimate of the total Fire Radiative Energy (FRE), which for wildfires should be proportional to the total mass of fuel biomass 
combusted.
STORAGE FOLDER: MSG_FTA_FRP_GRID

#########################################################################################################################################################################
								11. DAILY FRACTION OF VEGETATION COVER – MSG
#########################################################################################################################################################################
DESCRIPTION: Fractional Vegetation Cover (FVC) defines an important structural property of a plant canopy, which corresponds to the complement to unity of the gap 
fraction at nadir direction, accounting for the amount of vegetation distributed in a horizontal perspective. FVC is related with the partition between soil and 
vegetation contribution for emissivity and temperature. This property is necessary for describing land surface processes and surface parameterisation schemes used for 
climate and weather forecasting. Besides, the FVC is relevant for a wide range of Land Biosphere Applications such as agriculture and forestry, environmental management 
and land use, hydrology, natural hazards monitoring and management, vegetation-soil dynamics monitoring, drought conditions and fire scar extent.
STORAGE FOLDER: MSG_FVC

#########################################################################################################################################################################
								12. DAILY LEAF AREA INDEX – MSG
#########################################################################################################################################################################
DESCRIPTION: Leaf Area Index (LAI) is a dimensionless variable [m2/m2], which defines an important structural property of a plant canopy. LAI is defined as one half the 
total leaf area per unit ground area (Chen and Black, 1992). It provides complementary information to the FVC, accounting for the surface of leaves contained in a 
vertical column normalized by its cross-sectional area. It defines thus the area of green vegetation that interacts with solar radiation determining the remote sensing 
signal, and represents the size of the interface between the vegetation canopy and the atmosphere for energy and mass exchanges. LAI is thus a necessary input for 
Numerical Weather Prediction (NWP), regional and global climate modelling, weather forecasting and global change monitoring.
STORAGE FOLDER: MSG_LAI

#########################################################################################################################################################################
								13. LAND SURFACE TEMPERATURE – MSG
#########################################################################################################################################################################
DESCRIPTION: Land Surface Temperature (LST) is the radiative skin temperature over land. LST plays an important role in the physics of land surface as it is involved in 
the processes of energy and water exchange with the atmosphere. LST is useful for the scientific community, namely for those dealing with meteorological and climate 
models. Accurate values of LST are also of special interest in a wide range of areas related to land surface processes, including meteorology, hydrology, 
agrometeorology, climatology and environmental studies
STORAGE FOLDER: MSG_LST

#########################################################################################################################################################################
								14. REFERENCE EVAPOTRANSPIRATION - MSG
#########################################################################################################################################################################
DESCRIPTION: Reference evapotranspiration, ETo, is the evapotranspiration rate from a clearly defined reference
surface. The concept was introduced to allow the estimation of the evaporative demand of the atmosphere independently of crop type, crop development or management 
practices. ETo corresponds to the evapotranspiration from a hypothetical extensive well-watered field covered with 12 cm height green grass having an albedo of 0.23 
would experience under the given down-welling short-wave radiation.
STORAGE FOLDER: MSG_METREF

#########################################################################################################################################################################
								15. SNOW COVER – MSG
#########################################################################################################################################################################
DESCRIPTION: Snow Cover (SC) is the presence of snow over land. SC plays an important role in the physics of land surface as it is involved in the processes of energy 
and water exchange with the atmosphere. SC is useful for the scientific community, namely for those dealing with meteorological and climate models. Accurate detection 
of snow in a pixel is also important for a wide range of areas related to land surface processes, including meteorology, hydrology, climatology and environmental studies.
STORAGE FOLDER: MSG_SC2

"""

info_tpc1 = """"
																				Available Data Products in A1C-TPC-1 Channel: 5 Products    

#########################################################################################################################################################################
								1. REFINED OCEAN PRODUCTS - AQUA - AMESD REGIONS
#########################################################################################################################################################################
DESCRIPTION: These are ocean products for the AMESD regions of the African coastline and are the MODIS 'refined mode' version of the near-real-time (NRT) products 
already distributed under the AMESD project. The refined mode versions use accurate atmospheric measurements vs. estimates in the NRT and are produced after a week 
or two delay. Regional data is available for the Indian Ocean: east and north east of Madagascar, Cape Verde, Mozambique, Nigeria, South Somalia (SSomalia) and 
Tanzania. Can be used free of charge, but may not be (re-)sold. Please acknowledge PML in publications and notify rsg@pml.ac.uk.
STORAGE FOLDER: AQUA_ROPMAD

#########################################################################################################################################################################
								2. COMPOSITE OCEAN PRODUCTS - MULTIMISSION - AMESD REGIONS
#########################################################################################################################################################################
DESCRIPTION: These products are 3-day composites of the MODIS near-real-time ocean products. These are combined versions of all satellite passes over an area within the 
compositing period. Part of the EAMNET and AMESD projects. Regional data is available for east and north east of Madagascar, Cape Verde, Mozambique, Nigeria, South 
Somalia (SSomalia) and Tanzania. Can be used free of charge, but may not be (re-)sold. Please acknowledge PML in publications and notify rsg@pml.ac.uk.
STORAGE FOLDER: MODIS_CPMAD

#########################################################################################################################################################################
								3. OCEAN COLOUR PRODUCTS - MODIS – AQUA
#########################################################################################################################################################################
DESCRIPTION: MODIS Aqua SST and Ocean Colour products. Daily at 1 km resolution, OC3v6 default products: Chlorophyll-A, Kd490, fluorescence line height. Regional data 
available for Angola, Ivory Coast, South Africa (East), Guinea, Namibia, Somalia (North), Senegal, South Africa (South), Tanzania or South Africa (West).
STORAGE FOLDER: MODIS_OCPUCT

#########################################################################################################################################################################
								4. NEAR REAL-TIME OCEAN PRODUCTS - MULTIMISSION - AMESD REGIONS
#########################################################################################################################################################################
DESCRIPTION: Near real-time (NRT) products from NASA's MODIS (Aqua) sensor, including chlorophyll-a, sea surface temperature, K490 (turbidity) and water leaving 
radiances. Part of the EAMNET and AMESD projects. Regional data is available for east and north east of Madagascar, Cape Verde, Mozambique, Nigeria, South Somalia 
(SSomalia) and Tanzania. Can be used free of charge, but may not be (re-)sold. Please acknowledge PML in publications and notify rsg@pml.ac.uk.
STORAGE FOLDER: MULT_NRTOMAD

#########################################################################################################################################################################
								5. NEAR REAL-TIME OCEAN PRODUCTS - MULTIMISSION – AFRICA
#########################################################################################################################################################################
DESCRIPTION: Mapped ocean data products from NASA's MODIS (Aqua) sensor, including chlorophyll-a, sea surface temperature, K490 (turbidity) and water leaving 
radiances. Regional data available for Algeria, Egypt, Ghana, Libya, Mozambique, Morocco (North), Red Sea, Sierra Leone, or Morocco (South). Part of the EAMNET and 
AMESD projects. Can be used free of charge, but may not be (re-)sold. Please acknowledge PML in publications and notify rsg@pml.ac.uk.
STORAGE FOLDER: MULT_NRTOMAD

"""

info_tpc5 = """
																		Available Data Products in A1C-TPC-5 Channel: 6 Products    

#########################################################################################################################################################################
								1. SOIL WATER INDEX - METOP – AFRICA
#########################################################################################################################################################################
DESCRIPTION: The Soil Water index (SWI) product provides continental daily information about moisture conditions in different soil layers. SWI daily images are produced 
from EUMETSAT ASCAT-25km SSM product in orbit format and include a quality flag indicating the availability of SSM measurements for SWI calculations. Soil moisture is a 
key parameter in numerous environmental studies including hydrology, meteorology and agriculture. In addition to Surface Soil Moisture (SSM), information on the moisture 
condition within the underlying soil profile is of interest for different applications. Soil moisture in plant root zone can be estimated by an infiltration model using 
information on surface soil moisture and soil characteristics.
STORAGE FOLDER: Metop_SWI
  

#########################################################################################################################################################################
								2. BURNT AREA - PROBA-V – AFRICA
#########################################################################################################################################################################
DESCRIPTION: BA or Burnt Area products include information on the first date of burn area since the start of the fire season (1st April), as stored in the so-called BA-
DAY dataset, and on the temporal pattern of the fire activity. The input data are daily surface reflectances of PROBA-V VEGETATION sensor. The burnt areas are surfaces 
which have been sufficiently affected by fire to display significant changes in the vegetation cover (destruction of dry material, reduction or loss of green material) 
and in the ground surface (temporarily darker because of ash). As fire can occur in any type of environmental context, the properties of the burnt surface may differ 
significantly from place to place. Therefore, their identification is based on a combination of surface's properties and change detection, i.e. differences in spectral 
properties before and after the fire occurrence, following refined L3JRC/GBA2000 methods. The BA product is generated every 10 days over Africa as part of the Geoland2 
BioPar core mapping service. 
STORAGE FOLDER: PROBA_V_BA

#########################################################################################################################################################################
								3. NORMALISED DIFFERENCE VEGETATION INDEX (NDVI) – SENTINEL-3 – AFRICA
#########################################################################################################################################################################
DESCRIPTION: A ratio of the intensity of light reflected off the Earth's surface in the visible and near-infrared spectral wavelengths, which quantifies the 
photosynthetic capacity of the vegetation in a given pixel of land surface. The input reflectances are corrected for cloud and snow, geometry, atmospheric perturbations 
and directional effects. From the available global product, this product is a geographic subset over Africa. Access to Copernicus Land Service products is free and open 
to all users. 
STORAGE FOLDER: NDVIA

#########################################################################################################################################################################
								4. WATER BODIES V1 - PROBA-V – AFRICA
#########################################################################################################################################################################
DESCRIPTION: Version 1 of Water bodies describes the state of small ponds in dry regions. The Global Vegetation Monitoring Unit of JRC has developed a method to map and 
monitor small inland water bodies in arid regions using low resolution satellite imagery from the VEGETATION instrument. Although this instrument provides images of the 
Earth with a 1-km resolution, it was demonstrated that it is sufficient to accurately map and monitor the presence of water in natural and artificial ponds and swamps 
of about 1 sq km in size. The accuracy obtained is in the order of 90%, i. e. 90% of the water bodies detected with the method over an area of 1 million 1 sq km were 
found to be correct. 
STORAGE FOLDER: PROBA_V_SWB

#########################################################################################################################################################################
								5. VEGETATION CONDITION INDEX - PROBA-V – AFRICA
#########################################################################################################################################################################
DESCRIPTION: The Vegetation Condition Indicator (VCI) is a categorical type of difference vegetation index. The VCI compares the observed NDVI to the range of values 
observed in the same period in previous years. The VCI is expressed in % and gives an idea where the observed value is situated between the extreme values (minimum and 
maximum) in the previous years. Lower and higher values indicate bad and good vegetation state conditions, respectively. 
STORAGE FOLDER: PROBA_V_VCI

#########################################################################################################################################################################
								6. WATER BODIES V2 - PROBA-V - SOUTH AMERICA
#########################################################################################################################################################################
DESCRIPTION: Version 2 of Water bodies (WB) is a 10-day synthesis product that detects inland water bodies across the globe by calculating 10-daily Mean Composites from 
daily Top-Of-Canopy reflectance inputs, performing a colorimetric transformation from RGB to HSV colour space and applying different thresholds for the Hue and Value 
component. 
STORAGE FOLDER: PROBA_V_SWB

"""

info_tpc6 = """
 									 									Available Data Products in A1C-TPC-6 Channel: 19 Products    

#########################################################################################################################################################################
								1. CHLOROPHYLL ALPHA (MODIS, MAPPED 4KM) – AQUA
#########################################################################################################################################################################
DESCRIPTION: MODIS provides the unprecedented ability to measure chlorophyll fluorescence, which gives insight into the health of phytoplankton in the ocean. When 
phytoplankton are under stress, they no longer photosynthesize and begin to emit absorbed sunlight as fluorescence. Measurements of the chlorophyll fluorescence can 
be used to describe the physiological state of the phytoplankton, help to determine the cause of phytoplankton bloom collapses and help to make more robust estimates 
of primary productivity on a global scale.
STORAGE FOLDER: AQUA_CHLORA

#########################################################################################################################################################################
								2. DUST DRY DEPOSITION - NMMB/BSC-DUST MODEL
#########################################################################################################################################################################
DESCRIPTION: Forecast of dust dry deposition for lead times between 12 and 72 hours every 6 hours.
STORAGE FOLDER: DUST_DDD

#########################################################################################################################################################################
								3. DUST FORECAST - MODEL
#########################################################################################################################################################################
DESCRIPTION: 72-hour forecast of different parameters associated with airborne mineral dust. Model: NMMB/BSCDust.
STORAGE FOLDER: DUST_DF

#########################################################################################################################################################################
								4. DUST LOAD - NMMB/BSC-DUST MODEL
#########################################################################################################################################################################
DESCRIPTION: Forecast of columnar dust load for lead times between 12 and 72 hours every 6 hours.
STORAGE FOLDER: DUST_DLO

#########################################################################################################################################################################
								5. DUST OPTICAL DEPTH AT 550 NM - NMMB/BSC-DUST MODEL
#########################################################################################################################################################################
DESCRIPTION: Forecast of dust optical depth at 550 nm for lead times between 12 and 72 hours every 6 hours.
STORAGE FOLDER: DUST_DOD

#########################################################################################################################################################################
								6. DUST SURFACE CONCENTRATION - NMMB/BSC-DUST MODEL
#########################################################################################################################################################################
DESCRIPTION: Forecast of dust surface concentration for lead times between 12 and 72 hours every 6 hours.
STORAGE FOLDER: DUST_DSC

#########################################################################################################################################################################
								7. DUST SURFACE EXTINCTION AT 550 NM - NMMB/BSC-DUST MODEL
#########################################################################################################################################################################
DESCRIPTION: Forecast of dust optical depth at 550 nm for lead times between 12 and 72 hours every 6 hours.
STORAGE FOLDER: DUST_DSE

#########################################################################################################################################################################
								8. DUST WET DEPOSITION - NMMB/BSC-DUST MODEL
#########################################################################################################################################################################
DESCRIPTION: Forecast of dust wet deposition for lead times between 12 and 72 hours every 6 hours.
STORAGE FOLDER: DUST_DWD

#########################################################################################################################################################################
								9. UG-MESA POTENTIAL FISHING ZONE MAPS
#########################################################################################################################################################################
DESCRIPTION: The PFZ chart is developed from a Generalized Additive Model built from a binomial distribution family with a probit link function. Parameters for 
developing the model were presence- absence data of fish catch data from logbooks and a suite of environmental datasets covering the equatorial Atlantic. The charts 
are generated daily with surface temperature (SST), sea surface heights (SSH), geostrophic currents (UV) and salinity (SSS) datasets as inputs into the model. The PFZ 
chart shows the probability of occurrence of pelagic fish in the equatorial Atlantic. The pixel values range from 0% to 100% which indicates the probability of 
finding the optimal conditions preferred by pelagic fishes.
STORAGE FOLDER: MESA_UG_PFZ

#########################################################################################################################################################################
								10. SEA SURFACE SALINITY FORECAST - WEST AFRICA
#########################################################################################################################################################################
DESCRIPTION: Forecast maps of sea surface salinity (SAL) are generated by the ECOWAS Coastal and Marine Resources Management Centre from data obtained from the 
Operational Mercator global Ocean analysis system via the Copernicus programme at a resolution of 1/12 (0.08) degree. Forecasting of ocean weather is done for a 7-day 
period including a nowcast product for the present day. The forecast products are generated daily with a geographical area coverage of latitude 10 degrees south to 30 
degrees north and longitude 35 degrees west to 15 degrees east. This covers the coastal and oceanic waters of western Africa. Forecast products are updated daily for 
the seventh day (number of files per day = 1). Further information about this forecast data can be obtained from www.marine.copernicus.eu.
STORAGE FOLDER: MESA_UG_SAL

#########################################################################################################################################################################
								11. SEA SURFACE CURRENTS FORECAST - WEST AFRICA
#########################################################################################################################################################################
DESCRIPTION: Forecast maps of sea surface currents (SSC) are generated by the ECOWAS Coastal and Marine Resources Management Centre from data obtained from the 
Operational Mercator global Ocean analysis system via the Copernicus programme at a resolution of 1/12 (0.08) degree. Forecasting of ocean weather is done for a 7-day 
period including a nowcast product for the present day. The forecast products are generated daily with a geographical area coverage of latitude 10 degrees south to 30 
degrees north and longitude 35 degrees west to 15 degrees east. This covers the coastal and oceanic waters of western Africa. Forecast products are updated daily for 
the seventh day (number of files per day = 1). Further information about this forecast data can be obtained from www.marine.copernicus.eu.
STORAGE FOLDER: MESA_UG_SSC

#########################################################################################################################################################################
								12. SEA SURFACE HEIGHTS FORECAST - WEST AFRICA
#########################################################################################################################################################################
DESCRIPTION: Forecast maps of sea surface height (SSH), are generated by the ECOWAS Coastal and Marine Resources Management Centre from data obtained from the 
Operational Mercator global Ocean analysis system via the Copernicus programme at a resolution of 1/12 (0.08) degree. Forecasting of ocean weather is done for a 7-day 
period including a nowcast product for the present day. The forecast products are generated daily with a geographical area coverage of latitude 10 degrees south to 30 
degrees north and longitude 35 degrees west to 15 degrees east. This covers the coastal and oceanic waters of western Africa. Forecast products are updated daily for 
the seventh day (number of files per day = 1). Further information about this forecast data can be obtained from www.marine.copernicus.eu.
STORAGE FOLDER: MESA_UG_SSH

#########################################################################################################################################################################
								13. WAVE HEIGHT FORECAST - WEST AFRICA
#########################################################################################################################################################################
DESCRIPTION: Charts of wave forecast are generated from operational wave ensemble forecast produced by the National centre for Environmental Prediction (NCEP) of the 
National Oceanic and Atmospheric Administration (NOAA). The forecast data is produced using global AWIPS grid with a resolution of 0.5 degrees. NCEP wave forecasts 
products are produced for a 5-day period on hourly bases. Daily average of wave forecasts are however generated for the 5 days from the hourly products by the ECOWAS 
Coastal and Marine Resources Management Centre. The forecast products are generated daily with a geographical area coverage of latitude 10 degrees south to 30 degrees 
north and longitude 35 degrees west to 15 degrees east. This covers the coastal and oceanic waters of western Africa. Five (5) files are generated daily for the five 
forecasts days. Further information about this forecast data can be obtained from http://www.nco.ncep.noaa.gov/pmb/products/wave/.
STORAGE FOLDER: MESA_UG_SWH

#########################################################################################################################################################################
								14. SEA SURFACE TEMPERATURE FORECAST - WEST AFRICA
#########################################################################################################################################################################
DESCRIPTION: Forecast maps of sea surface temperature (SST) are generated by the ECOWAS Coastal and Marine Resources Management Centre from data obtained from the 
Operational Mercator global Ocean analysis system via the Copernicus programme at a resolution of 1/12 (0.08) degree. Forecasting of ocean weather is done for a 7-day 
period including a nowcast product for the present day. The forecast products are generated daily with a geographical area coverage of latitude 10 degrees south to 30 
degrees north and longitude 35 degrees west to 15 degrees east. This covers the coastal and oceanic waters of western Africa. Forecast products are updated daily for 
the seventh day (number of files per day = 1). Further information about this forecast data can be obtained from www.marine.copernicus.eu.
STORAGE FODLER: MESA-UG_SST

#########################################################################################################################################################################
								15. PHOTOSYNTHETICALLY AVAILABLE RADIATION – MODIS
#########################################################################################################################################################################
DESCRIPTION: The algorithm estimates daily average photosynthetically available radiation (PAR) at the ocean surface in Einstein m-2 d-1. PAR is defined as the quantum 
energy flux from the Sun in the 400-700nm range. For ocean color applications, PAR is a common input used in modeling marine primary productivity.
STORAGE FOLDER: MODIS_MOD_PAR

#########################################################################################################################################################################
								16. DIFFUSE ATTENUATION COEFFICIENT FOR DOWNWELLING IRRADIANCE AT 490 NM – MODIS
#########################################################################################################################################################################
DESCRIPTION: The algorithm returns the diffuse attenuation coefficient for downwelling irradiance at 490 nm (Kd_490) in m-1, calculated using an empirical relationship 
derived from in situ measurements of Kd_490 and blue-to-green band ratios of remote sensing reflectances (Rrs).
STORAGE FOLDER: MODIS_MOD-KD-490

#########################################################################################################################################################################
								17. LONG-WAVE SEA SURFACE TEMPERATURE – MODIS
#########################################################################################################################################################################
DESCRIPTION: NASA standard processing and distribution of the Sea Surface Temperature (SST) products from the MODIS sensors is now performed using software developed by 
the Ocean Biology Processing Group (OBPG). The OBPG generates Level-2 SST products using the Multi-Sensor Level-1 to Level-2 software (l2gen), which is the same 
software used to generate MODIS ocean color products. The longwave SST algorithm makes use of MODIS bands 31 and 32 at 11 and 12 nm. The brightness 
temperatures are derived from the observed radiances by inversion (in linear space) of the radiance versus blackbody temperature relationship. 
STORAGE FOLDER: MODIS_MOD-SST
#########################################################################################################################################################################
								18. RAINFALL ESTIMATE FOR AFRICA – MSG
#########################################################################################################################################################################
DESCRIPTION: Dekadal (every 10 days) and monthly rainfall estimates and anomalies derived from Meteosat Thermal Infra-Red (TIR) channels based on the recognition of 
storm clouds and calibration against ground-based rain gauge data
STORAGE FOLDER: MSG_RFE

#########################################################################################################################################################################
								19. IMAGE DATA – LANDSAT
#########################################################################################################################################################################
DESCRIPTION: Land application products for Central Africa from OSFAC (Observatoire Satellital des Forêts d'Afrique Centrale). Landsat L1T (terrain corrected) data from 
the Landsat 7 satellite. The Level 1T (L1T) data product provides systematic radiometric and geometric accuracy by incorporating ground control points, while also 
employing a Digital Elevation Model (DEM) for topographic accuracy. Geodetic accuracy of the product depends on the accuracy of the ground control points and the 
resolution of the DEM used. All Landsat 7 scenes collected since May of 2003 have data gaps. Although the scenes have only 78 percent of their pixels, these data are 
still some of the most geometrically and radiometrically accurate of all civilian satellite data in the world.
STORAGE FOLDER: UMDL1T

#########################################################################################################################################################################
								20. WAVE WATCH III PRODUCTS - MODEL - NORTH ATLANTIC OCEAN
#########################################################################################################################################################################
DESCRIPTION: Maps of swell (height, period and direction) of the model WAVE WATCH III Version 2.22 until 60 hours of forecasting with 1°*1° of resolution.
STORAGE FOLDER: WW3NAO

"""

info_tpg1 = """
																		Available Data Products in A1C-TPG-1 Channel: 31 Products    

#########################################################################################################################################################################
								1. ATMOSPHERIC MOTION VECTORS IR1 AND IR3 - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Atmospheric motion vectors (AMVs) are a valuable observation type for providing dynamical information for forecast models. They are produced by tracking 
clouds or gradients in water vapour through successive satellite images. AMVs have been assimilated in forecast models since the 1980s. Traditionally they are generated 
using imagery from geostationary satellites, which monitor a constant region of the Earth. AMVs are produced at several centres including EUMETSAT in Europe, NESDIS in 
the USA, JMA in Japan, CMA in China and IMD in India.
STORAGE FOLDER: FY2G_AMV

#########################################################################################################################################################################
								2. CLOUD CLASSIFICATION PRODUCT - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Cloud Classification Product.
STORAGE FOLDER: FY2G_CLT

#########################################################################################################################################################################
								3. TOTAL CLOUD AMOUNT PRODUCT - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Total Cloud Amount Product.
STORAGE FOLDER: FY2G_CTA

#########################################################################################################################################################################
								4. HUMIDITY PRODUCT ANALYSED BY CLOUD INFORMATION - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Humidity product analysed by cloud information Product.
STORAGE FOLDER: FY2G_HPF

#########################################################################################################################################################################
								5. OUTGOING LONGWAVE RADIATION PRODUCT - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Outgoing Longwave Radiation Product - 3 hours; 5, 10 and 30 days.
STORAGE FOLDER: FY2G_OLR

#########################################################################################################################################################################
								6. PRECIPITATION ESTIMATION PRODUCT - 6 & 24 HOURS - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Precipitation estimation product - 6 and 24 hours.
STORAGE FOLDER: FY2G_PRE
#########################################################################################################################################################################
								7. SURFACE SOLAR IRRADIANCE PRODUCT - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Surface Solar Irradiance Product.
STORAGE FOLDER: FY2G_SSI

#########################################################################################################################################################################
								8. BLACKBODY BRIGHTNESS TEMPERATURE - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Blackbody brightness temperature products are disseminated on an hourly, daily, 5-day, 10-day and 30-day basis
STORAGE FOLDER: FY2G_TBB

#########################################################################################################################################################################
								9. TOTAL PRECIPITABLE WATER PRODUCT - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Total Precipitable Water Product.
STORAGE FOLDER: FY2G_TPW

#########################################################################################################################################################################
								10. SNOW FRACTION PRODUCT - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Snow Fraction Product for FengYun 2G.
STORAGE FOLDER: FY2G_TSG

#########################################################################################################################################################################
								11. NORMALIZED GEOSTATIONARY PROJECTION DATASET - FENG-YUN - 2G
#########################################################################################################################################################################
DESCRIPTION: Full disk images from the Chinese satellite FengYun 2G.
STORAGE FOLDER: FY2G_FDI

#########################################################################################################################################################################
								12. ATMOSPHERIC MOTION VECTORS IR1 AND IR3 - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Atmospheric motion vectors (AMVs) are a valuable observation type for providing dynamical information for forecast models. They are produced by tracking 
clouds or gradients in water vapour through successive satellite images. AMVs have been assimilated in forecast models since the 1980s. Traditionally they are generated 
using imagery from geostationary satellites, which monitor a constant region of the Earth. AMVs are produced at several centres including EUMETSAT in Europe, NESDIS in 
the USA, JMA in Japan, CMA in China and IMD in India.
STORAGE FOLDER: FY2H_AMV

#########################################################################################################################################################################
								13. CLOUD CLASSIFICATION PRODUCT - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Cloud Classification Product.
STORAGE FOLDER: FY2H_CLT

#########################################################################################################################################################################
								14. TOTAL CLOUD AMOUNT PRODUCT - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Total Cloud Amount Product.
STORAGE FOLDER: FY2H_CTA

#########################################################################################################################################################################
								15. HUMIDITY PRODUCT ANALYSED BY CLOUD INFORMATION - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Humidity product analysed by cloud information Product.
STORAGE FOLDER: FY2H_HPF

#########################################################################################################################################################################
								16. OUTGOING LONGWAVE RADIATION PRODUCT - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Outgoing Longwave Radiation Product - 3 hours; 5, 10 and 30 days.
STORAGE FOLDER: FY2H_OLR

#########################################################################################################################################################################
								17. PRECIPITATION ESTIMATION PRODUCT - 6 & 24 HOURS - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Precipitation estimation product - 6 and 24 hours.
STORAGE FOLDER: FY2H_PRE
#########################################################################################################################################################################
								18. SURFACE SOLAR IRRADIANCE PRODUCT - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Surface Solar Irradiance Product.
STORAGE FOLDER: FY2H_SSI

#########################################################################################################################################################################
								19. BLACKBODY BRIGHTNESS TEMPERATURE - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Blackbody brightness temperature products are disseminated on an hourly, daily, 5-day, 10-day and 30-day basis
STORAGE FOLDER: FY2H_TBB

#########################################################################################################################################################################
								20. TOTAL PRECIPITABLE WATER PRODUCT - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Total Precipitable Water Product.
STORAGE FOLDER: FY2H_TPW

#########################################################################################################################################################################
								21. SNOW FRACTION PRODUCT - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Snow Fraction Product for FengYun 2H.
STORAGE FOLDER: FY2H_TSG

#########################################################################################################################################################################
								22. NORMALIZED GEOSTATIONARY PROJECTION DATASET - FENG-YUN - 2H
#########################################################################################################################################################################
DESCRIPTION: Full disk images from the Chinese satellite FengYun 2H.
STORAGE FOLDER: FY2H_FDI

#########################################################################################################################################################################
								23. QUANTITATIVE PRECIPITATION ESTIMATION (GOES PRECIPITATION INDEX) - INSAT-3D
#########################################################################################################################################################################
DESCRIPTION: Rainfall from INSAT-3D Imager channels is derived based on two methodologies: (i) Rainfall Estimation by GOES Precipitation Index (GPI) (ii) INSAT 
Multispectral Rainfall Algorithm.
STORAGE FOLDER: INSAT3D_GPI

#########################################################################################################################################################################
								24. HYDRO ESTIMATOR PRECIPITATION - INSAT-3D
#########################################################################################################################################################################
DESCRIPTION: This product is derived on the basis of Hydro-Estimator method. It measures precipitation over Indian Region encompassing the area between longitudes 30°E 
-to130°E and latitudes 50°N - 50°S.
STORAGE FOLDER: INSAT3D_HEM

#########################################################################################################################################################################
								25. RAIN RATE (INSAT MULTI-SPECTRAL RAINFALL) - INSAT-3D
#########################################################################################################################################################################
DESCRIPTION: Indian Multi Spectral rainfall from IMAGER.
STORAGE FOLDER: INSAT3D_IMR

#########################################################################################################################################################################
								26. CLOUD MOTION VECTORS (INFRA-RED WIND) - INSAT-3D
#########################################################################################################################################################################
DESCRIPTION: Cloud Classification Product.
STORAGE FOLDER: INSAT3D_IRW

#########################################################################################################################################################################
								27. OUTGOING LONGWAVE RADIATION - INSAT-3D
#########################################################################################################################################################################
DESCRIPTION: Total outgoing longwave radiation (OLR) flux, thermally emitted from earth atmosphere system, is estimated by applying regression equation relating OLR flux 
with INSAT-3D Imager observed WV and thermal infrared radiances. The coefficients of the regression equations are determined from results of the Radiative Transfer
Model simulation with various atmospheric conditions.
STORAGE FOLDER: INSAT3D_OLR

#########################################################################################################################################################################
								28. HUMIDITY AND TEMPERATURE PROFILES, OVER INDIAN REGION (A1) AND INDIAN OCEAN (A2) - INSAT-3D
#########################################################################################################################################################################
DESCRIPTION: Sounder Level2 data for A1 and A2 sectors.
STORAGE FOLDER: INSAT3D_SND

#########################################################################################################################################################################
								29. SEA SURFACE TEMPERATURE - INSAT-3D
#########################################################################################################################################################################
DESCRIPTION: Sea surface temperature is derived from split thermal window channels (TIR1, TIR2) during daytime and using additional mid IR window channel (MIR) during 
night time over cloud free oceanic regions. The most important part of the SST retrieval from IR observations is the atmospheric correction, especially over tropics. 
This correction is determined through a suitable characterization of tropical atmospheres in radiative transfer model to simulate the brightness temperatures of 
INSAT-3D channels.
STORAGE FOLDER: INSAT3D_SST

#########################################################################################################################################################################
								30. UPPER TROPOSPHERIC HUMIDITY - INSAT-3D
#########################################################################################################################################################################
DESCRIPTION: Upper Tropospheric Humidity from IMAGER.
STORAGE FOLDER: INSAT3D_UTH

#########################################################################################################################################################################
								31. WATER VAPOUR WINDS - INSAT-3D
#########################################################################################################################################################################
DESCRIPTION: Water vapour derived wind vectors.
STORAGE FOLDER: INSAT3D_WVW

"""
# ______________________________________________________________________________
# Constants
new = 1
url = "https://eoric.uenr.edu.gh/wp-content/uploads/2022/03/GEONETCAST-Data-Products-2022.pdf"

logger = logging.getLogger(__name__)


# ______________________________________________________________________________
# Functions
def doNothing():
    print("nothing to do")
    logger.log(logging.INFO, "Nothing to do")


def openweb():
    webbrowser.open(url, new=new)


def view_logs():
    View_Window = tk.Tk()
    View_Window.title('Log Messages')
    View_Window.geometry('1360x500')
    # View_Window.iconbitmap(r"eoriclogo.ico")
    log = ScrolledText(View_Window, width=167, height=30)
    log.grid(column=0, row=0)


def about_info():
    tk.messagebox.showinfo('About', 'Version 1.0')


def tbox_select_all(tbox_list):
    for i in tbox_list:
        if not i.instate(['selected']):
            i.invoke()


def tbox_deselect_all(tbox_list):
    for i in tbox_list:
        if i.instate(['selected']):
            i.invoke()


def more_info(title, text):
    View_Window = tk.Tk()
    View_Window.title(title)
    View_Window.geometry('1360x850')
    # View_Window.iconbitmap(r"eoriclogo.ico")
    log = ScrolledText(View_Window, width=169, height=50)
    log.grid(column=0, row=0)

    tf = text
    log.insert(END, tf)


def epsg_info():
    head = 'A1C-EPS-G Channel Information'
    txt = info_epsg
    more_info(head, txt)


def geo3_info():
    head = 'A1C-GEO-3 Channel Information'
    txt = info_geo3
    more_info(head, txt)


def geo4_info():
    head = 'A1C-GEO-4 Channel Information'
    txt = info_geo4
    more_info(head, txt)


def rds1_info():
    head = 'A1C-RDS-1 Channel Information'
    txt = info_rds1
    more_info(head, txt)


def saf1_info():
    head = 'A1C-SAF-1 Channel Information'
    txt = info_saf1
    more_info(head, txt)


def saf2_info():
    head = 'A1C-SAF-2 Channel Information'
    txt = info_saf2
    more_info(head, txt)


def tpc1_info():
    head = 'A1C-TPC-1 Channel Information'
    txt = info_tpc1
    more_info(head, txt)


def tpc5_info():
    head = 'A1C-TPC-5 Channel Information'
    txt = info_tpc5
    more_info(head, txt)


def tpc6_info():
    head = 'A1C-TPC-6 Channel Information'
    txt = info_tpc6
    more_info(head, txt)


def tpg1_info():
    head = 'A1C-TPG-1 Channel Information'
    txt = info_tpg1
    more_info(head, txt)


def sort(sourcePath, desPath, channels):
    global failed, success, desFilePath, channel
    logger.info('Sorting starting...')
    for index in channels:

        sourceOverwrite = True
        name, ext, folder, channel = channels[index].values()
        # print(path)

        for r, d, f in os.walk(sourcePath):
            failed = []
            success = 0
            for file in f:
                if name and ext in file:
                    # print(file, " | ", folder, " | ", channel, " | ", 'exists')
                    filePath = os.path.join(r, file)
                    desFolderPath = desPath + "/" + channel
                    if not os.path.exists(desFolderPath):
                        os.makedirs(desFolderPath)

                    folderPath = os.path.join(desFolderPath, folder)
                    # print(folderPath)
                    if not os.path.exists(folderPath):
                        # print("Creating " + folder + '...')
                        msg = "Creating " + folder + '...'
                        logger.log(logging.WARNING, msg)
                        os.makedirs(folderPath)
                    modTime = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))

                    FolderName = str(modTime.year) + str(modTime.month).zfill(2)
                    FolderPath = os.path.join(folderPath, FolderName)
                    # print(FolderPath)
                    # msg = FolderPath
                    # logger.log(logging.INFO, msg)

                    # Check if folder exists, else make it
                    if not os.path.exists(FolderPath):
                        os.makedirs(FolderPath)
                    # print (file)

                    try:
                        desFilePath = os.path.join(FolderPath, file)
                        desFileSize = os.path.getsize(desFilePath)
                        srcFileSize = os.path.getsize(filePath)

                        if os.path.exists(desFilePath) and (desFileSize == srcFileSize):

                            # print('The file: \n' + file + '\n already exists in the destination')
                            # print('.\nDeleting duplicate at source...')
                            # msg = 'The file: \n' + file + '\n already exists in the destination' + '.\nDeleting duplicate at source...'
                            # logger.log(logging.INFO, msg)

                            os.remove(filePath)

                            # Check if file is gone
                            if not os.path.exists(filePath):
                                # print('Duplicate deleted.\n\n')
                                continue
                            else:
                                # print('Duplicate deletion failed for')
                                # print(file)
                                # print('/n/n')
                                msg = 'Duplicate deletion failed for \n' + file + '/n/n'
                                logger.log(logging.WARNING, msg)
                                failed.append(file)
                        # If duplicate files exist, use the sourceOvewrite to select precedence
                        elif os.path.exists(desFilePath) and (desFileSize != srcFileSize):

                            if sourceOverwrite:

                                # Use copy2 instead of copy or copyfile to preserve file metadata
                                # http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
                                # print('Copying.. ' + str(file))
                                msg = 'Copying.. ' + str(file)
                                logger.log(logging.INFO, msg)
                                shutil.copy2(filePath, desFilePath)
                                success += 1
                                # print('Done.')
                                msg = 'Done'
                                logger.log(logging.INFO, msg)

                                # print('Deleting source file...')
                                # msg = 'Deleting source file...'
                                # logger.log(logging.INFO, msg)
                                os.remove(filePath)

                                # Check if file is gone
                                if not os.path.exists(filePath):
                                    # print('Source file deleted.\n\n')
                                    # msg = 'Source file deleted.\n\n'
                                    # logger.log(logging.INFO, msg)
                                    continue
                                else:
                                    # print('Source deletion failed for \n')
                                    # print(file)
                                    # print('/n/n')
                                    msg = 'Source deletion failed for \n' + file + '/n/n'
                                    logger.log(logging.WARNING, msg)
                                    failed.append(file)

                            else:
                                # Don't copy to destination
                                # print('Deleting source file...')
                                # msg = 'Deleting source file...'
                                # logger.log(logging.INFO, msg)
                                os.remove(filePath)

                                # Check if file is gone
                                if not os.path.exists(filePath):
                                    # print('Source file deleted.\n\n')
                                    # msg = 'Source file deleted.\n\n'
                                    # logger.log(logging.INFO, msg)
                                    continue
                                else:
                                    # print('Source deletion failed for \n')
                                    # print(file)
                                    # print('/n/n')
                                    msg = 'Source deletion failed for \n' + file + '/n/n'
                                    logger.log(logging.WARNING, msg)
                                    failed.append(file)

                    except:
                        # File does not already exist
                        # Use copy2 instead of copy or copyfile to preserve file metadata
                        # http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
                        # print('Copying.. ' + str(file))
                        msg = 'Copying.. ' + str(file)
                        logger.log(logging.INFO, msg)
                        shutil.copy2(filePath, desFilePath)
                        success += 1
                        # print('Done.')
                        msg = 'Copying.. ' + str(file)
                        logger.log(logging.INFO, msg)
                        # print('Deleting source file...')
                        # msg = 'Deleting source file...'
                        # logger.log(logging.INFO, msg)
                        os.remove(filePath)

                        # Check if file is gone
                        if not os.path.exists(filePath):
                            # print('Source file deleted.\n\n')
                            # msg = 'Source file deleted.\n\n'
                            # logger.log(logging.INFO, msg)
                            continue
                        else:
                            # print('Source deletion failed for \n')
                            # print(file)
                            # print('/n/n')
                            msg = 'Source deletion failed for \n' + file + '/n/n'
                            logger.log(logging.WARNING, msg)
                            failed.append(file)

    if len(failed) == 0:
        # print("Sorting Complete!")
        # print(str(success) + " file(s) successfully sorted.")
        msg = "Sorting Complete for " + channel + ' Channel:' + str(success) + " file(s) successfully sorted."
        logger.log(logging.INFO, msg)
        # print('Completed in: {}'.format(endTime - startTime))

    else:
        # print("Sorting Complete!")
        # print(str(success) + " file(s) successfully sorted.")
        # print('Completed in: {}'.format(endTime - startTime))
        # print('\n')
        # print('The following files could not be deleted')
        msg = "Sorting Complete! \n" + str(
            success) + " file(s) successfully sorted.\n The following files could not be deleted"
        logger.log(logging.INFO, msg)
        for x in failed:
            # print(x)
            msg = x
            logger.log(logging.INFO, msg)


# ______________________________________________________________________________
class QueueHandler(logging.Handler):

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


# ______________________________________________________________________________
class DirectoriesUi:

    def __init__(self, frame):
        entry_width = 50
        pady = 10
        padx = 10

        self.frame = frame
        global SF_entry, DF_entry
        self.SourceFolder = StringVar(value="C:/EUMETCast/received/afr-1")
        self.des_Folder = StringVar(value="C:/EUMETCast/received/sorted")

        # Creating content for Directories frame
        self.SF_label = ttk.Label(self.frame, text='Source Folder')
        SF_entry = ttk.Entry(self.frame, width=entry_width, textvariable=self.SourceFolder)
        self.browse_sf_btn = ttk.Button(self.frame, text='Browse...', command=self.browse_file_SF)

        self.DF_label = ttk.Label(self.frame, text='Destination Folder')
        DF_entry = ttk.Entry(self.frame, width=entry_width, textvariable=self.des_Folder)
        self.browse_df_btn = ttk.Button(self.frame, text='Browse...', command=self.browse_file_DF)

        self.SF_label.grid(row=0, column=0, pady=pady)
        SF_entry.grid(row=0, column=1, pady=pady)
        self.browse_sf_btn.grid(row=0, column=2, padx=5, pady=pady)

        self.DF_label.grid(row=1, column=0, pady=pady)
        DF_entry.grid(row=1, column=1, pady=pady)
        self.browse_df_btn.grid(row=1, column=2, padx=padx, pady=pady)

    def browse_file_SF(self):
        SF_name = filedialog.askdirectory()
        if SF_name is not None:
            self.SourceFolder.set(str(SF_name))

    def browse_file_DF(self):
        DF_name = filedialog.askdirectory()
        if DF_name is not None:
            self.des_Folder.set(str(DF_name))


# ______________________________________________________________________________
class ActivityUi:

    def __init__(self, frame):
        pady = 10
        padx = 10
        self.frame = frame

        self.start_btn = ttk.Button(self.frame, text='Start', command=run)
        self.start_btn.grid(row=0, column=5, padx=padx, pady=pady)

        # global pgbar
        # pgbar = ttk.Progressbar(self.frame, length=200, orient=HORIZONTAL, maximum=100, mode='determinate')
        # pgbar.grid(row=0, column=0, columnspan=4, padx=padx, pady=pady)

        global var
        var = StringVar()
        var.set('Application idle ...')
        status_label = ttk.Label(self.frame, width=13, text="Latest Activity: ")
        status_text = ttk.Label(self.frame, width=40, textvariable=var)
        status_label.grid(row=0, column=0, padx=padx, pady=pady)
        status_text.grid(row=0, column=1, columnspan=4, padx=padx, pady=pady)


# ______________________________________________________________________________
class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText widget

        self.scrolled_text = ScrolledText(frame, state='disabled', width=160, height=15)
        self.scrolled_text.grid(row=0, column=0)
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('WARNING', foreground='orange')

        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)

        # Start polling messages from the queue
        self.frame.after(1, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(1, self.poll_log_queue)


# ______________________________________________________________________________


class App:

    def __init__(self, root):
        pady = 10
        padx = 10
        width_all = 15

        self.root = root
        root.title("EORIC GEONETCast Data Sorter")
        root.geometry("1360x1080")

        # Creating Menu bar
        Main_menu = Menu(self.root)
        self.root.config(menu=Main_menu)

        # Creating the sub menus for File
        FileMenu = Menu(Main_menu)
        Main_menu.add_cascade(label='File', menu=FileMenu)
        # FileMenu.add_command(label='Start', command=doNothing)
        # FileMenu.add_command(label='Stop', command=doNothing)
        FileMenu.add_command(label='Exit', command=self.root.destroy)

        # Creating the sub menu for Help
        HelpMenu = Menu(Main_menu)
        Main_menu.add_cascade(label='Help', menu=HelpMenu)
        HelpMenu.add_command(label='Documentation', command=openweb)
        HelpMenu.add_command(label='About', command=about_info)

        # Creating frames to be used
        heading = Label(self.root, text="GEONETCAST DATA SORTER", font="Calibri 30")
        folderFrame = ttk.LabelFrame(self.root, text="DIRECTORIES")
        activityFrame = ttk.LabelFrame(self.root, text="ACTIVITY")
        channelsFrame = ttk.LabelFrame(self.root, text="CHANNELS (afr-1)")
        logsFrame = ttk.LabelFrame(self.root, text="LOGS")

        epsgFrame = ttk.LabelFrame(channelsFrame, text="A1C-EPS-G")
        geo3Frame = ttk.LabelFrame(channelsFrame, text="A1C-GEO-3")
        geo4Frame = ttk.LabelFrame(channelsFrame, text="A1C-GEO-4")
        rds1Frame = ttk.LabelFrame(channelsFrame, text="A1C-RDS-1")
        saf1Frame = ttk.LabelFrame(channelsFrame, text="A1C-SAF-1")
        saf2Frame = ttk.LabelFrame(channelsFrame, text="A1C-SAF-2")
        tpc1Frame = ttk.LabelFrame(channelsFrame, text="A1C-TPC-1")
        tpc5Frame = ttk.LabelFrame(channelsFrame, text="A1C-TPC-5")
        tpc6Frame = ttk.LabelFrame(channelsFrame, text="A1C-TPC-6")
        tpg1Frame = ttk.LabelFrame(channelsFrame, text="A1C-TPG-1")

        heading.grid(row=0, column=1, columnspan=4)
        folderFrame.grid(row=1, column=1, columnspan=2, padx=50, pady=5)
        activityFrame.grid(row=1, column=3, columnspan=2, padx=30, pady=5)
        channelsFrame.grid(row=2, column=1, columnspan=4, padx=10, pady=5)
        logsFrame.grid(row=3, column=1, columnspan=4, padx=30, pady=10)

        epsgFrame.grid(row=1, column=0, padx=padx, pady=pady)
        geo3Frame.grid(row=1, column=1, padx=padx, pady=pady)
        geo4Frame.grid(row=1, column=2, padx=padx, pady=pady)
        rds1Frame.grid(row=1, column=3, padx=padx, pady=pady)
        saf1Frame.grid(row=1, column=4, padx=padx, pady=pady)
        saf2Frame.grid(row=2, column=0, padx=padx, pady=pady)
        tpc1Frame.grid(row=2, column=1, padx=padx, pady=pady)
        tpc5Frame.grid(row=2, column=2, padx=padx, pady=pady)
        tpc6Frame.grid(row=2, column=3, padx=padx, pady=pady)
        tpg1Frame.grid(row=2, column=4, padx=padx, pady=pady)

        global EPSG_cb, GEO3_cb, GEO4_cb, RDS1_cb, SAF1_cb, SAF2_cb, TPC1_cb, TPC5_cb, TPC6_cb, TPG1_cb

        # ______________________________________________________________________________
        # Inserting content into epsgFrame (EPS-G)
        EPSG_cb = StringVar()
        cb1 = ttk.Checkbutton(epsgFrame, text="Sort Channel", width=width_all, variable=EPSG_cb,
                              onvalue="on", offvalue="off", )
        epsg_btn = ttk.Button(epsgFrame, text='More Info', command=epsg_info)
        cb1.grid(row=0, column=0, padx=padx, pady=pady)
        epsg_btn.grid(row=0, column=1, padx=padx, pady=pady)
        epsgFrame.grid(row=1, column=0, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into geo3Frame (GEO-3)
        GEO3_cb = StringVar()
        cb2 = ttk.Checkbutton(geo3Frame, text="Sort Channel", width=width_all, variable=GEO3_cb,
                              onvalue="on", offvalue="off", )
        geo3_btn = ttk.Button(geo3Frame, text='More Info', command=geo3_info)
        cb2.grid(row=0, column=0, padx=padx, pady=pady)
        geo3_btn.grid(row=0, column=1, padx=padx, pady=pady)
        geo3Frame.grid(row=1, column=1, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into geo4Frame (GEO-4)
        GEO4_cb = StringVar(geo4Frame)
        cb3 = ttk.Checkbutton(geo4Frame, text="Sort Channel", width=width_all, variable=GEO4_cb,
                              onvalue="on", offvalue="off", )
        geo4_btn = ttk.Button(geo4Frame, text='More Info', command=geo4_info)
        cb3.grid(row=0, column=0, padx=padx, pady=pady)
        geo4_btn.grid(row=0, column=1, padx=padx, pady=pady)
        geo4Frame.grid(row=1, column=2, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into rds1Frame (RDS-1)
        RDS1_cb = StringVar(rds1Frame)
        cb4 = ttk.Checkbutton(rds1Frame, text="Sort Channel", width=width_all, variable=RDS1_cb,
                              onvalue="on", offvalue="off", )
        rds1_btn = ttk.Button(rds1Frame, text='More Info', command=rds1_info)
        cb4.grid(row=0, column=0, padx=padx, pady=pady)
        rds1_btn.grid(row=0, column=1, padx=padx, pady=pady)
        rds1Frame.grid(row=1, column=3, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into saf1Frame (SAF-1)
        SAF1_cb = StringVar(saf1Frame)
        cb5 = ttk.Checkbutton(saf1Frame, text="Sort Channel", width=width_all, variable=SAF1_cb,
                              onvalue="on", offvalue="off", )
        saf1_btn = ttk.Button(saf1Frame, text='More Info', command=saf1_info)
        cb5.grid(row=0, column=0, padx=padx, pady=pady)
        saf1_btn.grid(row=0, column=1, padx=padx, pady=pady)
        saf1Frame.grid(row=1, column=4, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into saf2Frame (SAF-2)
        SAF2_cb = StringVar(saf2Frame)
        cb6 = ttk.Checkbutton(saf2Frame, text="Sort Channel", width=width_all, variable=SAF2_cb,
                              onvalue="on", offvalue="off", )
        saf2_btn = ttk.Button(saf2Frame, text='More Info', command=saf2_info)
        cb6.grid(row=0, column=0, padx=padx, pady=pady)
        saf2_btn.grid(row=0, column=1, padx=padx, pady=pady)
        saf2Frame.grid(row=2, column=0, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into tpc1Frame (TPC-1)
        TPC1_cb = StringVar(tpc1Frame)
        cb7 = ttk.Checkbutton(tpc1Frame, text="Sort Channel", width=width_all, variable=TPC1_cb,
                              onvalue="on", offvalue="off", )
        tpc1_btn = ttk.Button(tpc1Frame, text='More Info', command=tpc1_info)
        cb7.grid(row=0, column=0, padx=padx, pady=pady)
        tpc1_btn.grid(row=0, column=1, padx=padx, pady=pady)
        tpc1Frame.grid(row=2, column=1, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into tpc5Frame (TPC-5)
        TPC5_cb = StringVar(tpc5Frame)
        cb8 = ttk.Checkbutton(tpc5Frame, text="Sort Channel", width=width_all, variable=TPC5_cb,
                              onvalue="on", offvalue="off", )
        tpc5_btn = ttk.Button(tpc5Frame, text='More Info', command=tpc5_info)
        cb8.grid(row=0, column=0, padx=padx, pady=pady)
        tpc5_btn.grid(row=0, column=1, padx=padx, pady=pady)
        tpc5Frame.grid(row=2, column=2, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into tpc5Frame (TPC-6)
        TPC6_cb = StringVar(tpc6Frame)
        cb9 = ttk.Checkbutton(tpc6Frame, text="Sort Channel", width=width_all, variable=TPC6_cb,
                              onvalue="on", offvalue="off", )
        tpc6_btn = ttk.Button(tpc6Frame, text='More Info', command=tpc6_info)
        cb9.grid(row=0, column=0, padx=padx, pady=pady)
        tpc6_btn.grid(row=0, column=1, padx=padx, pady=pady)
        tpc6Frame.grid(row=2, column=3, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into tpg1Frame (TPG-1)
        TPG1_cb = StringVar(tpg1Frame)
        cb10 = ttk.Checkbutton(tpg1Frame, text="Sort Channel", width=width_all, variable=TPG1_cb,
                               onvalue="on", offvalue="off", )
        tpg1_btn = ttk.Button(tpg1Frame, text='More Info', command=tpg1_info)
        cb10.grid(row=0, column=0, padx=padx, pady=pady)
        tpg1_btn.grid(row=0, column=1, padx=padx, pady=pady)
        tpg1Frame.grid(row=2, column=4, padx=padx, pady=pady)

        # ______________________________________________________________________________
        tboxes_list = [cb1, cb2, cb3, cb4, cb5, cb6, cb7, cb8, cb9, cb10]
        # print(tboxes_list)
        for i in tboxes_list:
            i.invoke()
            i.invoke()

        # ______________________________________________________________________________
        # Inserting select all and deselect buttons

        deselect_all_tbox_button = ttk.Button(channelsFrame, text='Deselect all',
                                              command=lambda: tbox_deselect_all(tboxes_list))
        select_all_tbox_button = ttk.Button(channelsFrame, text='Select all',
                                            command=lambda: tbox_select_all(tboxes_list))

        select_all_tbox_button.grid(row=3, column=3, padx=padx, pady=pady, sticky=E)
        deselect_all_tbox_button.grid(row=3, column=4, padx=padx, pady=pady, sticky=W)

        stop_btn = ttk.Button(activityFrame, text='Quit', command=self.quit)
        stop_btn.grid(row=0, column=6, padx=padx, pady=pady)

        # Initialize all frames
        self.directories = DirectoriesUi(folderFrame)
        self.console = ConsoleUi(logsFrame)
        self.activity = ActivityUi(activityFrame)

        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)
        self.root.update_idletasks()

    def quit(self, *args):
        self.root.destroy()


# ______________________________________________________________________________
def sort(sourcePath, desPath, channels):
    global failed, success, desFilePath, channel, var
    # logger.info('Sorting starting...')
    for index in channels:

        sourceOverwrite = True
        name, ext, folder, channel = channels[index].values()
        # print(path)

        for r, d, f in os.walk(sourcePath):
            failed = []
            success = 0
            for file in f:
                if name and ext in file:
                    # print(file, " | ", folder, " | ", channel, " | ", 'exists')

                    filePath = os.path.join(r, file)
                    desFolderPath = desPath + "/" + channel
                    if not os.path.exists(desFolderPath):
                        os.makedirs(desFolderPath)

                    folderPath = os.path.join(desFolderPath, folder)
                    # print(folderPath)
                    if not os.path.exists(folderPath):
                        # print("Creating " + folder + '...')
                        msg = "Creating " + folder + '...'
                        logger.log(logging.WARNING, msg)
                        os.makedirs(folderPath)
                    modTime = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))

                    FolderName = str(modTime.year) + str(modTime.month).zfill(2)
                    FolderPath = os.path.join(folderPath, FolderName)
                    # print(FolderPath)
                    # msg = FolderPath
                    # logger.log(logging.INFO, msg)

                    # Check if folder exists, else make it
                    if not os.path.exists(FolderPath):
                        os.makedirs(FolderPath)
                    # print (file)

                    try:
                        desFilePath = os.path.join(FolderPath, file)
                        desFileSize = os.path.getsize(desFilePath)
                        srcFileSize = os.path.getsize(filePath)

                        if os.path.exists(desFilePath) and (desFileSize == srcFileSize):

                            # print('The file: \n' + file + '\n already exists in the destination')
                            # print('.\nDeleting duplicate at source...')
                            # msg = 'The file: \n' + file + '\n already exists in the destination' + '.\nDeleting duplicate at source...'
                            # logger.log(logging.INFO, msg)

                            os.remove(filePath)

                            # Check if file is gone
                            if not os.path.exists(filePath):
                                # print('Duplicate deleted.\n\n')
                                continue
                            else:
                                # print('Duplicate deletion failed for')
                                # print(file)
                                # print('/n/n')
                                msg = 'Duplicate deletion failed for \n' + file + '/n/n'
                                logger.log(logging.WARNING, msg)
                                failed.append(file)
                        # If duplicate files exist, use the sourceOvewrite to select precedence
                        elif os.path.exists(desFilePath) and (desFileSize != srcFileSize):

                            if sourceOverwrite:

                                # Use copy2 instead of copy or copyfile to preserve file metadata
                                # http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
                                # print('Copying.. ' + str(file))
                                msg = 'Copying.. ' + str(file)
                                logger.log(logging.INFO, msg)
                                shutil.copy2(filePath, desFilePath)
                                success += 1
                                # print('Done.')
                                msg = 'Done'
                                logger.log(logging.INFO, msg)

                                # print('Deleting source file...')
                                # msg = 'Deleting source file...'
                                # logger.log(logging.INFO, msg)
                                os.remove(filePath)

                                # Check if file is gone
                                if not os.path.exists(filePath):
                                    # print('Source file deleted.\n\n')
                                    # msg = 'Source file deleted.\n\n'
                                    # logger.log(logging.INFO, msg)
                                    continue
                                else:
                                    # print('Source deletion failed for \n')
                                    # print(file)
                                    # print('/n/n')
                                    msg = 'Source deletion failed for \n' + file + '/n/n'
                                    logger.log(logging.WARNING, msg)
                                    failed.append(file)

                            else:
                                # Don't copy to destination
                                # print('Deleting source file...')
                                # msg = 'Deleting source file...'
                                # logger.log(logging.INFO, msg)
                                os.remove(filePath)

                                # Check if file is gone
                                if not os.path.exists(filePath):
                                    # print('Source file deleted.\n\n')
                                    # msg = 'Source file deleted.\n\n'
                                    # logger.log(logging.INFO, msg)
                                    continue
                                else:
                                    # print('Source deletion failed for \n')
                                    # print(file)
                                    # print('/n/n')
                                    msg = 'Source deletion failed for \n' + file + '/n/n'
                                    logger.log(logging.WARNING, msg)
                                    failed.append(file)

                    except:
                        # File does not already exist
                        # Use copy2 instead of copy or copyfile to preserve file metadata
                        # http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
                        # print('Copying.. ' + str(file))
                        msg = 'Copying.. ' + str(file)
                        logger.log(logging.INFO, msg)
                        shutil.copy2(filePath, desFilePath)
                        success += 1
                        # print('Done.')
                        msg = 'Copying.. ' + str(file)
                        logger.log(logging.INFO, msg)
                        # print('Deleting source file...')
                        # msg = 'Deleting source file...'
                        # logger.log(logging.INFO, msg)
                        os.remove(filePath)

                        # Check if file is gone
                        if not os.path.exists(filePath):
                            # print('Source file deleted.\n\n')
                            # msg = 'Source file deleted.\n\n'
                            # logger.log(logging.INFO, msg)
                            continue
                        else:
                            # print('Source deletion failed for \n')
                            # print(file)
                            # print('/n/n')
                            msg = 'Source deletion failed for \n' + file + '/n/n'
                            logger.log(logging.WARNING, msg)
                            failed.append(file)

    if len(failed) == 0:
        # print("Sorting Complete!")
        # print(str(success) + " file(s) successfully sorted.")
        msg = "Sorting Complete for " + channel + ' Channel:' + str(success) + " file(s) successfully sorted."
        logger.log(logging.INFO, msg)
        # print('Completed in: {}'.format(endTime - startTime))

    else:
        # print("Sorting Complete!")
        # print(str(success) + " file(s) successfully sorted.")
        # print('Completed in: {}'.format(endTime - startTime))
        # print('\n')
        # print('The following files could not be deleted')
        msg = "Sorting Complete! \n" + str(
            success) + " file(s) successfully sorted.\n The following files could not be deleted"
        logger.log(logging.INFO, msg)
        for x in failed:
            # print(x)
            msg = x
            logger.log(logging.INFO, msg)


# ______________________________________________________________________________
def run():
    state_epsg = EPSG_cb.get()
    state_geo3 = GEO3_cb.get()
    state_geo4 = GEO4_cb.get()
    state_rds1 = RDS1_cb.get()
    state_saf1 = SAF1_cb.get()
    state_saf2 = SAF2_cb.get()
    state_tpc1 = TPC1_cb.get()
    state_tpc5 = TPC5_cb.get()
    state_tpc6 = TPC6_cb.get()
    state_tpg1 = TPG1_cb.get()
    s_name = SF_entry.get()
    d_name = DF_entry.get()

    worker = {"state_epsg": {"state": state_epsg, 'channel': 'A1C-EPS-G'},
              "state_geo3": {"state": state_geo3, 'channel': 'A1C-GEO-3'},
              "state_geo4": {"state": state_geo4, 'channel': 'A1C-GEO-4'},
              "state_rds1": {"state": state_rds1, 'channel': 'A1C-RDS-1'},
              "state_saf1": {"state": state_saf1, 'channel': 'A1C-SAF-1'},
              "state_saf2": {"state": state_saf2, 'channel': 'A1C-SAF-2'},
              "state_tpc1": {"state": state_tpc1, 'channel': 'A1C-TPC-1'},
              "state_tpc5": {"state": state_tpc5, 'channel': 'A1C-TPC-5'},
              "state_tpc6": {"state": state_tpc6, 'channel': 'A1C-TPC-6'},
              "state_tpg1": {"state": state_tpg1, 'channel': 'A1C-TPG-1'},
              }
    xx = 0.05
    xx_msg = ' Channel sorting completed ...'
    for state in worker:
        cb_state, channel_set = worker[state].values()

        if channel_set == 'A1C-EPS-G' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            time.sleep(xx)

            sort(sourcePath=s_name, desPath=d_name, channels=EPSG)

        if channel_set == 'A1C-GEO-3' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=GEO3)
            time.sleep(xx)

        if channel_set == 'A1C-GEO-4' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=GEO4)
            time.sleep(xx)

        if channel_set == 'A1C-RDS-1' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=RDS1)
            time.sleep(xx)

        if channel_set == 'A1C-SAF-1' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=SAF1)
            time.sleep(xx)

        if channel_set == 'A1C-SAF-2' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=SAF2)
            time.sleep(xx)

        if channel_set == 'A1C-TPC-1' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=TPC1)
            time.sleep(xx)

        if channel_set == 'A1C-TPC-5' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=TPC5)
            time.sleep(xx)

        if channel_set == 'A1C-TPC-6' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=TPC6)
            time.sleep(xx)

        if channel_set == 'A1C-TPG-1' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=TPG1)
            time.sleep(xx)


# ______________________________________________________________________________

def main():
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()
