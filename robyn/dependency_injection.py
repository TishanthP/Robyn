""" This is Robyn's dependency injection file.
"""
from robyn.robyn import (
    Response,
    Request,
)


class DependencyMap:
    def __init__(self):
        #'request' and 'response' mappings are needed for when constructing deps_to_pass in router.py
        self.global_dependency_map = {"request": Request, "response": Response}
        # {'router': {'dependency_name': dependency_class}
        self.router_dependency_map = {"request": Request, "response": Response}

    def add_router_dependency(self, router, **kwargs):
        """Adds a dependency to a route.

        Args:
            router App Object: The route to add the dependency to.
            kwargs (dict): The dependencies to add to the route.
        """
        if router not in self.router_dependency_map:
            self.router_dependency_map[router] = {}

        self.router_dependency_map[router].update(**kwargs)

    def add_global_dependency(self, **kwargs):
        """Adds a dependency to all routes.

        Args:
            kwargs (dict): The dependencies to add to all routes.
        """
        for name, element in kwargs.items():
            self.global_dependency_map.update({name: element})

    def get_router_dependencies(self, router):
        """Gets the dependencies for a specific route.

        Args:
            router

        Returns:
            dict: The dependencies for the specified route.
        """
        if route in self.router_dependency_map:
            return self.router_dependency_map[route]
        else:
            raise KeyError(f"Route '{route}' not found in dependencies.")

    def get_global_dependencies(self):
        """Gets the dependencies for a route.

        Args:
            route (str): The route to get the dependencies for.
        """
        return self.global_dependency_map

    def merge_dependencies(self, target_router):
        """
        Merge dependencies from this DependencyMap into another router's DependencyMap.

        Args:
            target_router: The router with which to merge dependencies.

        This method iterates through the dependencies of this DependencyMap and adds any dependencies
        that are not already present in the target router's DependencyMap.
        """
        for dep_key in self.get_global_dependencies():
            if dep_key in target_router.dependencies.get_global_dependencies():
                continue
            target_router.dependencies.get_global_dependencies()[dep_key] = self.get_global_dependencies()[dep_key]

    @property
    def dependency_map(self):
        return self.router_dependency_map