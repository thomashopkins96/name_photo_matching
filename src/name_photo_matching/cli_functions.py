from sgqlc.endpoint.http import HTTPEndpoint
import base64
from utils import to_csv
import os
from dotenv import load_dotenv


class CultsProducts:
    load_dotenv()

    def __init__(self):
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")

        self.token = base64.b64encode(str.encode(f"{self.user}:{self.password}")).decode()
        self.headers = {
                'Authorization': 'Basic ' + self.token,
                'User-Agent': 'GraphQL API client'
        }

        self.url = 'https://cults3d.com/graphql'
        self.endpoint = HTTPEndpoint(self.url, self.headers)

    def get_uploaded_products(self, limit: int = 10):
        query = '''
            {
                myself {
                    creationsBatch(limit:{0}, offset: 0) {
                        results {
                            name(locale: EN)
                            url(locale: EN)
                            downloadsCount
                            viewsCount
                            totalSalesAmount(currency: USD) { cents }
                            blueprints {
                                fileUrl
                                imageUrl
                            }
                        }
                    }
                }
            }
        '''

        query = query.format(limit)

        variables = {}

        try:
            data = self.endpoint(query, variables)

            return data

        except Exception as e:
            import traceback

            print(f"Error occurred: {e}")

            traceback.print_exc()

    def upload_new_product(self,
                           name,
                           description,
                           image_urls,
                           file_urls,
                           category_id,
                           subcategory_ids,
                           price,
                           visibility):

        mutation = """
        mutation CreateCreation(
          $name: String!,
          $description: String!,
          $details: String!,
          $imageUrls: [String!]!,
          $fileUrls: [String!]!,
          $categoryId: ID!,
          $subCategoryIds: [ID!]!,
          $downloadPrice: Float!,
          $visibility: Visibility!
        ) {
          createCreation(
            name: $name,
            description: $description,
            details: $details,
            imageUrls: $imageUrls,
            fileUrls: $fileUrls,
            locale: EN,
            categoryId: $categoryId,
            subCategoryIds: $subCategoryIds,
            downloadPrice: $downloadPrice,
            current: USD,
            licenseCode: "cults_cu",
            visibility: $visibility
          ) {
            creation { url(locale: EN) }
            errors
          }
        }
        """

        details = (
            "Mold box is one piece, does not require supports.\n"
            "Intended for FDM printers.\n\n"
            "- Temperature: Use higher-end of recommended temperature based on your material for best layer adhesion\n"
            "- Infill: Use higher infill to increase reusability of the mold box, usually 10% is sufficient\n"
            "- Infill Type: Cubic for speed and durability, Lightning for speed over durability\n"
            "- Walls: Use 3-4 walls if silicone is leaking inside of the print\n"
            "- Layer Height: 0.28mm, it is not necessary to have small layer heights unless layer lines along the inside of the mold are an issue\n"
            "- Bed temperature: 60C if using PLA, but user high-end of bed temperature for all materials to prevent warping\n\n"
            "Advanced Settings:\n"
            "- Top Surface Skin Layer: 1-2, this will help with a more smooth surface and better molds\n"
            "- Monotonic Top/Bottom Order: Enabled\n"
            "- Enable Ironing: Enabled, irons layer lines from top surfaces flat\n"
            "- Retract at Layer Change: Enabled, if scarring the top surface from the nozzle dragging is an issue"
        )

        variables = {
            "name": name,
            "description": description,
            "details": details,
            "imageUrls": image_urls,            # e.g. ["https://.../img1.jpg"]
            "fileUrls": file_urls,              # e.g. ["https://.../file1.stl"]
            "categoryId": category_id,          # match API type (string/ID)
            "subCategoryIds": subcategory_ids,  # list of IDs
            "downloadPrice": float(price),      # ensure number, not "2.95"
            "visibility": visibility            # e.g. "VISIBLE"
        }

        try:
            data = self.endpoint(mutation, variables)

            return data

        except Exception as e:
            import traceback

            print(f"Error occurred: {e}")

            traceback.print_exc()
