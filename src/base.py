import pandas as pd

class MbaE:
    """
    **Mba'e** in Guarani means **Thing**.

    .. important::

        **Mba'e is the origin**. The the very-basic almost-zero level object.
        Basically, it implements a method to return metadata as a DataFrame.
        Deeper than here is only the Python builtin ``object`` class.


    **Examples:**

    Here's how to use the ``MbaE`` class:

    Import ``MbaE``:

    .. code-block:: python

        # import the object
        from plans.src_root import MbaE

    ``MbaE`` instantiation

    .. code-block:: python

        # MbaE instantiation
        m = MbaE(name="Algo", alias="al")

    Retrieve metadata (not all attributes)

    .. code-block:: python

        # Retrieve metadata (not all attributes)
        d = m.get_metadata()
        print(d)

    Retrieve metadata in a `pandas.DataFrame`

    .. code-block:: python

        # Retrieve metadata in a `pandas.DataFrame`
        df = m.get_metadata_df()
        print(df.to_string(index=False))

    Set new values for metadata

    .. code-block:: python

        # Set new values for metadata
        d2 = {"Name": "Algo2", "Alias": "al2"}
        m.set(dict_setter=d2)

    Boot attributes from csv file:

    .. code-block:: python

        # Boot attributes from csv file:
        m.boot(bootfile="/content/metadata.csv")


    """

    def __init__(self, name: str="MyMbaE", alias: str | None=None):
        """Initialize the ``MbaE`` object.

        :param name: unique object name
        :type name: str

        :param alias: unique object alias.
            If None, it takes the first and last characters from ``name``
        :type alias: str

        """
        # ------------ pseudo-static ----------- #

        #
        self.object_name = self.__class__.__name__
        self.object_alias = "mbae"

        # name
        self.name: str = name

        # alias
        self.alias: str | None = alias

        # handle None alias
        if self.alias is None:
            self._create_alias()

        # fields
        self._set_fields()

        # ------------ set mutables ----------- #
        self.bootfile = None
        self.folder_bootfile = "./"  # start in the local place

        # ... continues in downstream objects ... #

    def __str__(self):
        """The ``MbaE`` string"""
        str_type = str(type(self))
        df = self.get_metadata_df()
        str_df_metadata: str = df.to_string(index=False)
        str_out = "[{} ({})]\n{} ({}):\t{}\n{}".format(
            self.name,
            self.alias,
            self.object_name,
            self.object_alias,
            str_type,
            str_df_metadata,
        )
        return str_out

    def _create_alias(self):
        """If ``alias`` is ``None``, it takes the first and last characters from ``name``"""
        if len(self.name) >= 2:
            self.alias = self.name[0] + self.name[len(self.name) - 1]
        else:
            self.alias = self.name[:]

    def _set_fields(self) -> None:
        """Set fields names"""

        # Attribute fields
        self.name_field = "Name"
        self.alias_field = "Alias"

        # Metadata fields
        self.mdata_attr_field = "Attribute"
        self.mdata_val_field = "Value"
        # ... continues in downstream objects ... #

    def get_metadata(self) -> dict[str, str]:
        """Get a dictionary with object metadata.

        .. note::

            Metadata does **not** necessarily inclue all object attributes.

        :return: dictionary with all metadata
        :rtype: dict
        """
        dict_meta = {
            self.name_field: self.name,
            self.alias_field: self.alias,
        }
        return dict_meta

    def get_metadata_df(self) -> pd.DataFrame:
        """Get a :class:`pandas.DataFrame` created from the metadata dictionary

        :return: :class:`pandas.DataFrame` with ``Attribute`` and ``Value``
        :rtype: :class:`pandas.DataFrame`
        """
        dict_metadata = self.get_metadata()
        df_metadata = pd.DataFrame(
            {
                self.mdata_attr_field: [k for k in dict_metadata],
                self.mdata_val_field: [dict_metadata[k] for k in dict_metadata],
            }
        )
        return df_metadata

    def set(self, dict_setter: dict):
        """Set selected attributes based on an incoming dictionary

        :param dict_setter: incoming dictionary with attribute values
        :type dict_setter: dict
        """
        # ---------- set basic attributes --------- #
        self.name = dict_setter[self.name_field]
        self.alias = dict_setter[self.alias_field]

        # ... continues in downstream objects ... #

    def boot(self, bootfile):
        """Boot fundamental attributes from a ``csv`` table.

        :param bootfile: file path to ``csv`` table with metadata information.
            Expected format:

            .. code-block:: text

                Attribute;Value
                Name;ResTia
                Alias;Ra

        :type bootfile: str

        :return:
        :rtype: str
        """
        # ---------- update file attributes ---------- #
        self.bootfile = bootfile[:]
        self.folder_bootfile = os.path.dirname(bootfile)

        # get expected fields
        list_columns = [self.mdata_attr_field, self.mdata_val_field]

        # read info table from ``csv`` file. metadata keys are the expected fields
        df_info_table = pd.read_csv(bootfile, sep=";", usecols=list_columns)

        # setter loop
        dict_setter = {}
        for i in range(len(df_info_table)):
            # build setter from row
            dict_setter[df_info_table[self.mdata_attr_field].values[i]] = df_info_table[
                self.mdata_val_field
            ].values[i]

        # pass setter to set() method
        self.set(dict_setter=dict_setter)

        return None
