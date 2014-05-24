from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger, Page

# This InfinitePager and InfinitePage class came from a reddit post
# but I cannot find the original reddit post or the site it linked to.
# I have only slightly modified it.
class InfinitePaginator(Paginator):
    """ HACK: To avoid unneseccary `SELECT COUNT(*) ...`
    paginator has an infinity page number and a count of elements.
    """
    def _get_num_pages(self):
        """
        Returns the total number of pages.
        """
        return float('inf')

    num_pages = property(_get_num_pages)

    def _get_count(self):
        """
        Returns the total number of objects, across all pages.
        """
        return float('inf')

    count = property(_get_count)

    def _get_page(self, *args, **kwargs):
        return InfinitePage(*args, **kwargs)


class InfinitePage(Page):
    def has_next(self):
        """ HACK: Select object_list + 1 element
        to verify next page existense.

        I think this could be made so thatthe query is just intended length + 1
        and then it just returns 1 less than the actual length and has_next checks that the
        length of that queryset is the full + 1 length
        """
        low = self.object_list.query.__dict__['low_mark']
        high = self.object_list.query.__dict__['high_mark']
        self.object_list.query.clear_limits()
        self.object_list.query.set_limits(low=low, high=high+1)

        try:
            # len is used only for small portions of data (one page)
            if len(self.object_list) <= self.paginator.per_page:
                return False

            return True
        finally:
            # restore initial object_list count
            self.object_list = self.object_list[:(high-low)]
