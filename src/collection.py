from .base import MbaE
import pandas as pd


class Collection(MbaE):
    """A collection of primitive ``MbaE`` objects with associated metadata.
    Useful for large scale manipulations in ``MbaE``-based objects.
    Expected to have custom methods and attributes downstream.

    **Main Attributes:**

    - ``catalog`` (:class:`pandas.DataFrame`): A catalog containing metadata of the objects in the test_collection.
    - ``collection`` (dict): A dictionary containing the objects in the ``Collection``.
    - name (str): The name of the ``Collection``.
    - alias (str): The name of the ``Collection``.
    - baseobject: The class of the base object used to initialize the ``Collection``.

    **Main Methods:**

    - __init__(self, base_object, name="myCatalog"): Initializes a new ``Collection`` with a base object.
    - update(self, details=False): Updates the ``Collection`` catalog.
    - append(self, new_object): Appends a new object to the ``Collection``.
    - remove(self, name): Removes an object from the ``Collection``.

    **Examples:**

    Here's how to use the `Collection` class:

    Import objects:

    .. code-block:: python

        # import MbaE-based object
        from plans.src_root import MbaE

        # import Collection
        from plans.src_root import Collection

    Instantiate ``Collection``:

    .. code-block:: python

        # instantiate Collection object
        c = Collection(base_object=MbaE, name="Collection")

    Append a new object to the ``Collection``:

    .. code-block:: python

        # append a new object
        m1 = MbaE(name="Thing1", alias="al1")
        c.append(m1)  # use .append()

    Append extra objects:

    .. code-block:: python

        # append extra objects
        m2 = MbaE(name="Thing2", alias="al2")
        c.append(m2)  # use .append()
        m3 = MbaE(name="Res", alias="r")
        c.append(m3)  # use .append()

    Print the catalog `pandas.DataFrame`:

    .. code-block:: python

        # print catalog `pandas.DataFrame`
        print(c.catalog)

    Print the collection dict:

    .. code-block:: python

        # print collection dict
        print(c.collection)

    Remove an object by using object name:

    .. code-block:: python

        # remove object by object name
        c.remove(name="Thing1")

    Apply MbaE-based methods for Collection

    .. code-block:: python

        # -- apply MbaE methods for Collection

        # reset metadata
        c.set(dict_setter={"Name": "Coll", "Alias": "C1"})

        # Boot attributes from csv file:
        c.boot(bootfile="/content/metadata_coll.csv")


    """

    def __init__(self, base_object, name="MyCollection", alias="Col0"):
        """Initialize the ``Collection`` object.

        :param base_object: ``MbaE``-based object for collection
        :type base_object: :class:`MbaE`

        :param name: unique object name
        :type name: str

        :param alias: unique object alias.
            If None, it takes the first and last characters from name
        :type alias: str

        """
        # ------------ call super ----------- #
        super().__init__(name=name, alias=alias)
        # ------------ set pseudo-static ----------- #
        self.object_alias = "COL"
        # Set the name and baseobject attributes
        self.baseobject = base_object
        self.baseobject_name = base_object.name

        # Initialize the catalog with an empty DataFrame
        dict_metadata = self.baseobject.get_metadata()

        self.catalog = pd.DataFrame(columns=dict_metadata.keys())

        # Initialize the ``Collection`` as an empty dictionary
        self.collection = dict()

        # ------------ set mutables ----------- #
        self.size = 0

        self._set_fields()
        # ... continues in downstream objects ... #

    def __str__(self):
        """
        The ``Collection`` string.
        Expected to overwrite superior methods.
        """
        str_type = str(type(self))
        str_df_metadata = self.get_metadata_df().to_string(index=False)
        str_df_data = self.catalog.to_string(index=False)
        str_out = "{}:\t{}\nMetadata:\n{}\nCatalog:\n{}\n".format(
            self.name, str_type, str_df_metadata, str_df_data
        )
        return str_out

    def _set_fields(self):
        """
        Set fields names.
        Expected to increment superior methods.
        """
        # ------------ call super ----------- #
        super()._set_fields()

        # Attribute fields
        self.size_field = "Size"
        self.baseobject_field = "Base_Object"  # self.baseobject().__name__

        # ... continues in downstream objects ... #

    def get_metadata(self):
        """Get a dictionary with object metadata.
        Expected to increment superior methods.

        .. note::

            Metadata does **not** necessarily inclue all object attributes.

        :return: dictionary with all metadata
        :rtype: dict
        """
        # ------------ call super ----------- #
        dict_meta = super().get_metadata()

        # customize local metadata:
        dict_meta_local = {
            self.size_field: self.size,
            self.baseobject_field: self.baseobject_name,
        }

        # update
        dict_meta.update(dict_meta_local)
        return dict_meta

    def update(self, details=False):
        """Update the ``Collection`` catalog.

        :param details: Option to update catalog details, defaults to False.
        :type details: bool
        :return: None
        :rtype: None
        """

        # Update details if specified
        if details:
            # Create a new empty catalog
            df_new_catalog = pd.DataFrame(columns=self.catalog.columns)

            # retrieve details from collection
            for name in self.collection:
                # retrieve updated metadata from base object
                dct_meta = self.collection[name].get_metadata()

                # set up a single-row helper dataframe
                lst_keys = dct_meta.keys()
                _dct = dict()
                for k in lst_keys:
                    _dct[k] = [dct_meta[k]]

                # Set new information
                df_aux = pd.DataFrame(_dct)

                # Append to the new catalog
                df_new_catalog = pd.concat([df_new_catalog, df_aux], ignore_index=True)

            # consider if the name itself has changed in the
            old_key_names = list(self.collection.keys())[:]
            new_key_names = list(df_new_catalog[self.catalog.columns[0]].values)

            # loop for checking consistency in collection keys
            for i in range(len(old_key_names)):
                old_key = old_key_names[i]
                new_key = new_key_names[i]
                # name change condition
                if old_key != new_key:
                    # rename key in the collection dictionary
                    self.collection[new_key] = self.collection.pop(old_key)

            # Update the catalog with the new details
            self.catalog = df_new_catalog.copy()
            # clear
            del df_new_catalog

        # Basic updates
        # --- the first row is expected to be the Unique name
        str_unique_name = self.catalog.columns[0]
        self.catalog = self.catalog.drop_duplicates(subset=str_unique_name, keep="last")
        self.catalog = self.catalog.sort_values(by=str_unique_name).reset_index(
            drop=True
        )
        self.size = len(self.catalog)
        return None

    # review ok
    def append(self, new_object):
        """Append a new object to the ``Collection``.

        The object is expected to have a ``.get_metadata()`` method that
        returns a dictionary with metadata keys and values

        :param new_object: Object to append.
        :type new_object: object

        :return: None
        :rtype: None
        """
        # Append a copy of the object to the ``Collection``
        copied_object = copy.deepcopy(new_object)
        self.collection[new_object.name] = copied_object

        # Update the catalog with the new object's metadata
        dct_meta = new_object.get_metadata()
        dct_meta_df = dict()
        for k in dct_meta:
            dct_meta_df[k] = [dct_meta[k]]
        df_aux = pd.DataFrame(dct_meta_df)

        # Check if self.catalog is empty before concatenation
        if self.catalog.empty:
            # If it's empty, just assign df_aux to self.catalog
            self.catalog = df_aux
        else:
            # If it's not empty, perform the concatenation
            self.catalog = pd.concat([self.catalog, df_aux], ignore_index=True)

        self.update()
        return None

    def remove(self, name):
        """Remove an object from the ``Collection`` by the name.

        :param name: Name attribute of the object to remove.
        :type name: str

        :return: None
        :rtype: None
        """
        # Delete the object from the ``Collection``
        del self.collection[name]
        # Delete the object's entry from the catalog
        str_unique_name = self.catalog.columns[
            0
        ]  # assuming the first column is the unique name
        self.catalog = self.catalog.drop(
            self.catalog[self.catalog[str_unique_name] == name].index
        ).reset_index(drop=True)
        self.update()
        return None

