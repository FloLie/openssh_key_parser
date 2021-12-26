import typing

from cryptography.hazmat.primitives.asymmetric import dsa

from openssh_key.pascal_style_byte_stream import (
    PascalStyleFormatInstruction,
    FormatInstructionsDict,
    ValuesDict
)

from .common import (
    PublicKeyParams,
    PrivateKeyParams,
    ConversionFunctions
)


class DSSPublicKeyParams(PublicKeyParams):
    """The parameters comprising a key in the Digital Signature Standard
    cryptosystem (FIPS 186).

    The names and iteration order of parameters of a *public* DSS key is:

    * ``p``: The public modulus (:any:`int`).
    * ``q``: The subgroup order (:any:`int`).
    * ``g``: The generator (:any:`int`).
    * ``y``: The public key (:any:`int`).

    NB: OpenSSH `has deprecated <https://www.openssh.com/legacy.html>`_ the
    "ssh-dss" public key algorithm. OpenSSH only supports DSS keys of length
    1024 bits, which are vulnerable to the
    `Logjam attack <https://weakdh.org/>`_.

    Args:
        params
            The values with which to initialize this parameters object. All
            given values are saved, even those that do not exist in the format
            instructions for this key type.

    Raises:
        UserWarning: A parameter value from the above list is missing from
            ``params`` or does not have the correct type.
    """
    FORMAT_INSTRUCTIONS_DICT: typing.ClassVar[FormatInstructionsDict] = {
        'p': PascalStyleFormatInstruction.MPINT,
        'q': PascalStyleFormatInstruction.MPINT,
        'g': PascalStyleFormatInstruction.MPINT,
        'y': PascalStyleFormatInstruction.MPINT,
    }

    @staticmethod
    def conversion_functions(
    ) -> typing.Mapping[
        typing.Type[typing.Any],
        ConversionFunctions
    ]:
        """Conversion functions for key objects of the following types:

        * :any:`cryptography.hazmat.primitives.asymmetric.dsa.DSAPublicKey`

        Returns:
            A :py:class:`typing.Mapping` from the above types of key objects
            to functions that take key objects of these types and return
            parameter values.
        """
        def dsa_public_key_convert_from_cryptography(
            key_object: dsa.DSAPublicKey
        ) -> ValuesDict:
            public_numbers = key_object.public_numbers()
            parameter_numbers = public_numbers.parameter_numbers
            return {
                'p': parameter_numbers.p,
                'q': parameter_numbers.q,
                'g': parameter_numbers.g,
                'y': public_numbers.y,
            }

        def dsa_public_key_convert_to_cryptography(
            key_params: ValuesDict
        ) -> dsa.DSAPublicKey:
            return dsa.DSAPublicNumbers(
                key_params['y'],
                dsa.DSAParameterNumbers(
                    key_params['p'],
                    key_params['q'],
                    key_params['g']
                )
            ).public_key()

        return {
            dsa.DSAPublicKey: ConversionFunctions(
                dsa_public_key_convert_from_cryptography,
                dsa_public_key_convert_to_cryptography
            )
        }


DSSPrivateKeyParamsTypeVar = typing.TypeVar(
    'DSSPrivateKeyParamsTypeVar',
    bound='DSSPrivateKeyParams'
)


class DSSPrivateKeyParams(PrivateKeyParams, DSSPublicKeyParams):
    """The parameters comprising a private key in the Digital Signature Standard
    cryptosystem (FIPS 186).

    The names and iteration order of parameters of a *private* DSS key is:

    * ``p``: The public modulus (:any:`int`).
    * ``q``: The subgroup order (:any:`int`).
    * ``g``: The generator (:any:`int`).
    * ``y``: The public key (:any:`int`).
    * ``x``: The private key (:any:`int`).

    NB: OpenSSH `has deprecated <https://www.openssh.com/legacy.html>`_ the
    "ssh-dss" public key algorithm. OpenSSH only supports DSS keys of length
    1024 bits, which are vulnerable to the
    `Logjam attack <https://weakdh.org/>`_.

    Args:
        params
            The values with which to initialize this parameters object. All
            given values are saved, even those that do not exist in the format
            instructions for this key type.

    Raises:
        UserWarning: A parameter value from the above list is missing from
            ``params`` or does not have the correct type.
    """

    FORMAT_INSTRUCTIONS_DICT: typing.ClassVar[FormatInstructionsDict] = {
        'p': PascalStyleFormatInstruction.MPINT,
        'q': PascalStyleFormatInstruction.MPINT,
        'g': PascalStyleFormatInstruction.MPINT,
        'y': PascalStyleFormatInstruction.MPINT,
        'x': PascalStyleFormatInstruction.MPINT,
    }

    KEY_SIZE = 1024

    @classmethod
    def generate_private_params(
        cls: typing.Type[DSSPrivateKeyParamsTypeVar],
        **kwargs: typing.Any
    ) -> DSSPrivateKeyParamsTypeVar:
        """Constructs and initializes a DSS private key parameters object
        with generated values.

        Args:
            kwargs
                Keyword arguments consumed to generate parameter values.

        Returns:
            A private key parameters object with generated values valid for
            a DSS private key (the key size is 128 bytes).
        """

        private_key = dsa.generate_private_key(DSSPrivateKeyParams.KEY_SIZE)

        private_numbers = private_key.private_numbers()
        public_numbers = private_numbers.public_numbers
        parameter_numbers = public_numbers.parameter_numbers

        return cls({
            'p': parameter_numbers.p,
            'q': parameter_numbers.q,
            'g': parameter_numbers.g,
            'y': public_numbers.y,
            'x': private_numbers.x,
        })

    @staticmethod
    def conversion_functions(
    ) -> typing.Mapping[
        typing.Type[typing.Any],
        ConversionFunctions
    ]:
        """Conversion functions for key objects of the following types:

        * :any:`cryptography.hazmat.primitives.asymmetric.dsa.DSAPrivateKey`

        Returns:
            A :py:class:`typing.Mapping` from the above types of key objects
            to functions that take key objects of these types and return
            parameter values.
        """
        def dsa_private_key_convert_from_cryptography(
            key_object: dsa.DSAPrivateKey
        ) -> ValuesDict:
            private_numbers = key_object.private_numbers()
            public_numbers = private_numbers.public_numbers
            parameter_numbers = public_numbers.parameter_numbers
            return {
                'p': parameter_numbers.p,
                'q': parameter_numbers.q,
                'g': parameter_numbers.g,
                'y': public_numbers.y,
                'x': private_numbers.x,
            }

        def dsa_private_key_convert_to_cryptography(
            key_params: ValuesDict
        ) -> dsa.DSAPrivateKey:
            return dsa.DSAPrivateNumbers(
                key_params['x'],
                dsa.DSAPublicNumbers(
                    key_params['y'],
                    dsa.DSAParameterNumbers(
                        key_params['p'],
                        key_params['q'],
                        key_params['g']
                    )
                )
            ).private_key()

        return {
            dsa.DSAPrivateKey: ConversionFunctions(
                dsa_private_key_convert_from_cryptography,
                dsa_private_key_convert_to_cryptography
            )
        }
