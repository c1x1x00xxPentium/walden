# This dataset download is a bit hard to automate, a human needs to follow the
# steps below instead:
#
# 1. Go to the GHDx results tool: http://ghdx.healthdata.org/gbd-results-tool
# 2a. For gbd_cause select the following:
#
#    Measure: Deaths; DALYs (Disability-Adjusted Life Years)
#    Age: All Ages; Age-standardized; Under 5; 5-14 years; 15-49 years; 50-69 years; 70+ years
#    Metric: Number; Rate; Percent
#    Year: select all
#    Cause: select all
#    Context: Cause
#    Sex: Both
#    Location: select all countries
#
# 2b. For gbd_child_mortality select the following:
#
#    Measure: Deaths; DALYs (Disability-Adjusted Life Years)
#    Age: Early Neonatal (0-6 days); Late Neonatal (7-27 days) - calculate 0-28 days; Post Neonatal (28-364 days); <1 year; 1-4 years
#    Metric: Number; Rate; Percent
#    Year: select all
#    Cause: Total All causes; A.1.1: HIV/AIDS; A.1.2: Sexually transmitted infections excluding HIV; A.1.2.1: Syphillis; A.2.1: Tuberculosis; A.2.2: Lower respiratory infections;
#           A.2.3: Upper respiratory infections, A.3: Enteric infections, A.3.1: Diarrheal diseases, A.3.2: Typhoid and paratyphoid, A.3.2.1: Typhoid fever, A.4.1: Malaria, A.5: Other infectious diseases and all under this,
#           A.6.2: Neonatal disorders and all under, A.7: Nutritional deficiencies, A.7.1: Protein-energy malnutrition, B.3: Chronic respiratory diseases, B.4: Digestive diseases, B.4.1 Cirrhosis and chronic liver diseases,
#           B.8 Diabetes and kidney diseases, B.12.1: Congenital birth defects and all under this, B.12.7: Sudden infant death syndrome
#    Context: Cause
#    Sex: Both; Male; Female
#    Location: select all countries
#    Permalink: http://ghdx.healthdata.org/gbd-results-tool?params=gbd-api-2019-permalink/fc24dcf060876044fe3d5702a101ec3f
#
# 2c. For gbd_mental_health select the following:
#
#    Measure: Prevalence
#    Age: All Ages; Age-standardized; Under 5; 5-14 years; 15-49 years; 50-69 years; 70+ years; 10 to 14; 15 to 19; 20 to 24; 25 to 29; 30 to 34
#    Metric: Number; Rate; Percent
#    Year: select all
#    Cause: All under B.6 - Mental Disorders; All under B.7 - Substance Use Disorders
#    Context: Cause
#    Location: select all countries
#    Sex: Both; Male; Female
#
# 2d. For gbd_prevalence select the following:
#
#    Measure: Prevalence; Incidence
#    Age: All Ages; Age-standardized; Under 5; 5-14 years; 15-49 years; 50-69 years; 70+ years
#    Metric: Number; Rate; Percent
#    Year: select all
#    Cause: select all
#    Context: Cause
#    Location: select all countries
#    Sex: Both
#
# 2e. For gbd_risk select the following:
#
#    Measure: Deaths; DALYs (Disability-Adjusted Life Years)
#    Age: All Ages; Age-standardized; Under 5; 5-14 years; 15-49 years; 50-69 years; 70+ years
#    Metric: Number; Percent; Rate
#    Year: select all
#    Risks: select all
#    Cause: Total All Causes; Cardiovascular diseases; Lower respiratory infections; Diarrheal diseases; Neoplasms
#    Context: Risk
#    Location: select all countries
#    Sex: Both
#
# 3. Wait for the data to be prepared and for a download link to be sent
import click
import os
import glob
import pandas as pd
from structlog import get_logger
from owid.walden import add_to_catalog


log = get_logger()


@click.command()
@click.option(
    "--upload/--skip-upload",
    default=True,
    type=bool,
    help="Upload dataset to Walden",
)
def main(upload: bool) -> None:
    names = ["gbd_cause", "gbd_risk", "gbd_prevalence", "gbd_child_mortality", "gbd_mental_health"]
    descriptions = ["Deaths and DALYs", "Risk factors", "Prevalence and incidence", "Child mortality", "Mental health"]
    for name, description in zip(names, descriptions):
        log.info("Combining data for:", df_name=name)
        outpath = combine_csvs(name=name, inpath="/Users/fionaspooner/Documents/temp/gbd_2021/gbd_cause/csv/")
        metadata = {
            "namespace": "ihme_gbd",
            "short_name": "%s" % (name),
            "description": "%s" % (description),
            "publication_year": 2019,
            "source_name": "Institute for Health Metrics and Evaluation - Global Burden of Disease Collaborative Network",
            "url": "https://vizhub.healthdata.org/gbd-results/",
            "file_extension": "feather",
            "license_url": "https://www.healthdata.org/data-tools-practices/data-practices/terms-and-conditions",
        }
        log.info("Adding data to catalog:", df_name=name)
        add_to_catalog(metadata=metadata, outpath=outpath, upload=upload, public=False)


def combine_csvs(name: str, inpath: str) -> str:
    # setting the path for joining multiple files
    files = os.path.join(inpath, "*.csv")
    # list of merged files returned
    files = glob.glob(files)
    # joining files with concat and read_csv
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    outpath = f"{inpath}/{name}.feather"
    df.to_feather(outpath)
    return str


if __name__ == "__main__":
    main()
