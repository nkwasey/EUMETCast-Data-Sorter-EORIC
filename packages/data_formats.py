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