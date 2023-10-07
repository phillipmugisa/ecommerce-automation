from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from product_scrapper.main import get_products
import concurrent.futures
from django.core.cache import cache

# Create your views here.
class HomeView(generic.View):
    template_name = "manager/index.html"

    def get(self, request):
        return render(request, template_name=self.template_name)

class ProductSearch(generic.View):
    template_name = "manager/product_list.html"

    def post(self, request):
        product_name = request.POST.get("product-name")
        platform_choice = request.POST.getlist("platform-choice")
        if not product_name:
            return HttpResponse(status=404)
        if not platform_choice:
            return HttpResponse(status=404)

        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [] # stores our running tasks/threads
            for choice in [choice.upper() for choice in platform_choice]:
                futures.append(executor.submit(get_products, product_name, choice))

            for future in concurrent.futures.as_completed(futures):
                try:
                    results.append(future.result())
                except:
                    pass

        # caching results to make filtering faster
        if cache.get("previous_search_results"):
            cache.delete("previous_search_results")
        cache.set("previous_search_results", results, 60 * 15)

        context_data = {"results" : results, "name": product_name}
        return render(request, template_name=self.template_name, context=context_data)


class PlatformFilterView(generic.View):
    template_name = "manager/product_list.html"

    def get(self, request, platform, product_name):
        if not platform:
            return HttpResponse(status=404)

        results = cache.get("previous_search_results")
        if not results:
            # no cache found. scrap products again
            try:
                results = get_products(product_name, platform)
                cache.set("previous_search_results", results, 60 * 15)
            except:
                return HttpResponse(status=404)

        for result in results:
            if result.get("platform").lower() != platform.lower():
                result["omit"] = True

        context_data = {"results" : results, "name": product_name}
        return render(request, template_name=self.template_name, context=context_data)