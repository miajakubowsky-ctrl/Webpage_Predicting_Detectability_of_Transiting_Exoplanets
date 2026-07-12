# this code allows the user to input the values they want to for the calculator

from pydantic import BaseModel

class CalculationRequest(BaseModel):
    D: float
    altitude: float
    airmass: float
    QE: float
    exposure_time: float
    read_noise: float
    sky_brightness: float
    pixel_size: float
    focal_length: float
    aperture_radius_pix: float
    dark_current_rate: float
    full_well: float
    vega_zp: float
    eff: float
    weff: float
    fwhm_optimistic: float
    fwhm_pessimistic: float
    magnitude_min: float
    magnitude_max: float
