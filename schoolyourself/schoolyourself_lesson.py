"""An XBlock that displays School Yourself lessons."""

import urllib

from xblock.core import XBlock
from xblock.fragment import Fragment

from schoolyourself import SchoolYourselfXBlock


class SchoolYourselfLessonXBlock(SchoolYourselfXBlock):
    """
    This block renders a launcher button for a School Yourself lesson,
    which is rendered in an iframe. The block transmits the anonymous
    user ID.
    """
    has_children = False
    has_score = False

    def student_view(self, context=None):
      """
      The primary view of the SchoolYourselfLessonXBlock, shown to students
      when viewing courses.
      """
      # Construct the URL we're going to stuff into the iframe once
      # it gets launched:
      url_params = self.get_partner_url_params(self.shared_key)
      url_params["id"] = self.module_id

      # Set up the screenshot URL:
      screenshot_url = "%s/page/screenshot/%s" % (self.base_url,
                                                  self.module_id)

      context = {
        "iframe_url": "%s/page/player?%s" % (self.base_url,
                                             urllib.urlencode(url_params)),
        "screenshot_url": screenshot_url
      }

      # Now actually render the fragment, which is just a button with
      # some JS code that handles the click event on that button.
      fragment = Fragment(self.render_template("student_view.html", context))

      # Load the common JS/CSS libraries:
      fragment.add_css_url(
        self.runtime.local_resource_url(self, "public/sylib.css"))
      fragment.add_javascript_url(
        self.runtime.local_resource_url(self, "public/sylib.js"))

      # And finally the embedded HTML/JS code:
      fragment.add_javascript(self.resource_string(
          "static/js/student_view.js"))
      fragment.add_css(self.resource_string(
          "static/css/student_view.css"))
      fragment.initialize_js("SchoolYourselfStudentView")
      return fragment


    @staticmethod
    def workbench_scenarios():
      """A canned scenario for display in the workbench."""
      return [
        ("SchoolYourselfLessonXBlock",
         """\
            <vertical_demo>
              <schoolyourself_lesson
                  module_id="geometry/lines_rays"
              />
            </vertical_demo>
         """),
        ]