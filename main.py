# This file takes website.py and runs it in your browser using FastAPI

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from website import min_depth
from values import CalculationRequest

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/api/calculate")
def calculate_api(request: CalculationRequest):
    result = min_depth(
        request.D, request.altitude, request.airmass, request.QE,
        request.exposure_time, request.read_noise, request.sky_brightness,
        request.pixel_size, request.focal_length, request.aperture_radius_pix,
        request.dark_current_rate, request.full_well, request.vega_zp,
        request.eff, request.weff, request.fwhm_optimistic,
        request.fwhm_pessimistic, request.magnitude_min, request.magnitude_max,
    )
    return result

# serve the form
@app.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse(request, "index.html", {"result": None})


# handle form submission
@app.post("/calculate", response_class=HTMLResponse)
def calculate_form(
    request: Request,
    D: float = Form(...),
    altitude: float = Form(...),
    airmass: float = Form(...),
    QE: float = Form(...),
    exposure_time: float = Form(...),
    read_noise: float = Form(...),
    sky_brightness: float = Form(...),
    pixel_size: float = Form(...),
    focal_length: float = Form(...),
    aperture_radius_pix: float = Form(...),
    dark_current_rate: float = Form(...),
    full_well: float = Form(...),
    vega_zp: float = Form(...),
    eff: float = Form(...),
    weff: float = Form(...),
    fwhm_optimistic: float = Form(...),
    fwhm_pessimistic: float = Form(...),
    magnitude_min: float = Form(...),
    magnitude_max: float = Form(...),
):
    calc_request = CalculationRequest(
        D=D, altitude=altitude, airmass=airmass, QE=QE,
        exposure_time=exposure_time, read_noise=read_noise,
        sky_brightness=sky_brightness, pixel_size=pixel_size,
        focal_length=focal_length, aperture_radius_pix=aperture_radius_pix,
        dark_current_rate=dark_current_rate, full_well=full_well,
        vega_zp=vega_zp, eff=eff, weff=weff,
        fwhm_optimistic=fwhm_optimistic, fwhm_pessimistic=fwhm_pessimistic,
        magnitude_min=magnitude_min, magnitude_max=magnitude_max,
    )

    result = min_depth(
        calc_request.D, calc_request.altitude, calc_request.airmass, calc_request.QE,
        calc_request.exposure_time, calc_request.read_noise, calc_request.sky_brightness,
        calc_request.pixel_size, calc_request.focal_length, calc_request.aperture_radius_pix,
        calc_request.dark_current_rate, calc_request.full_well, calc_request.vega_zp,
        calc_request.eff, calc_request.weff, calc_request.fwhm_optimistic,
        calc_request.fwhm_pessimistic, calc_request.magnitude_min, calc_request.magnitude_max,
    )

    return templates.TemplateResponse(request, "index.html", {"result": result})
