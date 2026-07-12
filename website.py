# This is the main calculator code (almost identical to previous versions) edited to be compatible with FastAPI

def min_depth(D,
         altitude,
         airmass,
         QE,
         exposure_time,
         read_noise,
         sky_brightness,
         pixel_size,
         focal_length,
         aperture_radius_pix,
         dark_current_rate,
         full_well,
         vega_zp,
         eff,
         weff,
         fwhm_optimistic,
         fwhm_pessimistic,
         magnitude_min,
         magnitude_max):

    import numpy as np
    from math import erf

    # ----------------- Derived -----------------
    A = np.pi * (D / 2) ** 2  # collecting area (m^2)
    n_pix_aperture = np.pi * aperture_radius_pix ** 2
    dark_current = dark_current_rate * exposure_time  # e-/pix for exposure
    pixel_scale = (pixel_size * 206) / focal_length
    magnitudes = np.linspace(magnitude_min, magnitude_max, 300)

    # ----------------- PSF fraction function -----------------
    def central_pixel_fraction(fwhm_px: float) -> float:
        """Fraction of a 2D Gaussian's total flux that lands in the central pixel
        when the star is centered on that pixel."""
        sigma = fwhm_px / (2.0 * np.sqrt(2.0 * np.log(2.0)))
        a = 0.5 / (np.sqrt(2.0) * sigma)
        return erf(a) ** 2


    # ----------------- Optimistic vs Pessimistic (make sure optimistic is BROADER) ----

    alpha_opt = central_pixel_fraction(fwhm_optimistic)
    alpha_pess = central_pixel_fraction(fwhm_pessimistic)

    # ----------------- Photon model -----------------
    E_phot = (6.63e-27 * 2.998e10) / (eff * 1e-8)  # erg per photon
    PFD = (vega_zp / E_phot) * weff * 10000  # photons/m^2/s for 0-mag star

    flux0 = PFD * QE * A * exposure_time  # electrons for a 0-mag star
    N_star = flux0 * 10 ** (-0.4 * magnitudes)  # total star electrons in aperture

    # sky
    sky_flux_density = PFD * 10 ** (-0.4 * sky_brightness)
    aperture_area_arcsec2 = n_pix_aperture * pixel_scale ** 2
    N_sky = sky_flux_density * QE * A * exposure_time * aperture_area_arcsec2
    sky_per_pixel = sky_flux_density * QE * A * exposure_time * (pixel_scale ** 2)

    # noise
    read_noise_total_var = (read_noise ** 2) * n_pix_aperture
    dc_total = dark_current * n_pix_aperture
    scint_frac = 0.00419 * D ** (-2 / 3) * airmass ** 1.75 * np.exp(-altitude / 8000) * exposure_time ** (-0.5)
    scint_noise = scint_frac * N_star
    noise_total = np.sqrt(N_star + N_sky + dc_total + read_noise_total_var + scint_noise ** 2)

    # SNR and min detectable depth
    snr = N_star / noise_total
    min_detectable_depth_ppt = (1 / snr) * 1000

    # ----------------- Saturation boundaries -----------------
    threshold = 0.8 * full_well


    def saturation_boundary(alpha):
        """Return the magnitude where peak pixel reaches threshold.
           If sky+dark already exceed threshold, returns -inf (everything saturates)."""
        F_lim = (threshold - (sky_per_pixel + dark_current)) / max(alpha, 1e-12)
        if F_lim <= 0:
            return -np.inf
        else:
            return -2.5 * np.log10(F_lim / max(flux0, 1e-30))


    m_sat_opt = saturation_boundary(alpha_opt)  # optimistic boundary (fewer saturations)
    m_sat_pess = saturation_boundary(alpha_pess)  # pessimistic boundary (more saturations)


    return {
        "magnitudes": magnitudes.tolist(),
        "min_detectable_depth_ppt": min_detectable_depth_ppt.tolist(),
        "snr": snr.tolist(),
        "m_sat_opt": float(m_sat_opt),
        "m_sat_pess": float(m_sat_pess)
    }
