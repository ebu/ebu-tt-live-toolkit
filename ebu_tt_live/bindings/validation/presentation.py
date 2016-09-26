from ebu_tt_live.errors import SemanticValidationError
from ebu_tt_live.strings import ERR_SEMANTIC_STYLE_MISSING, ERR_SEMANTIC_VALIDATION_EXPECTED, \
    ERR_SEMANTIC_REGION_MISSING


class SizingValidationMixin(object):
    """
    This is meant to validate that the sizing types correspond to the tt element and head region definitions.
    It is meant to be used by the containing element and its attributes as well so the class interoperates with itself.
    """

    def _semantic_check_sizing_type(self, value, dataset):
        """
        The sizing attribute is checked by the element for a value and attribute validation is ran as required.
        :param value: The sizing value to be checked
        :param dataset: The semantic dataset
        """
        if value is not None and isinstance(value, SizingValidationMixin):
            value._semantic_validate_sizing_context(dataset=dataset)

    def _semantic_validate_sizing_context(self, dataset):
        """
        The attribute can check if it is valid in the context provided by dataset
        :param dataset: The semantic dataset
        :raises SimpleTypeValueError
        """
        raise NotImplementedError()


class StyledElementMixin(object):
    """
    This functionality applies to all styled boxes to help computing styling related information
    """
    _compatible_style_type = None
    _referenced_styles = None
    _validated_styles = None
    _inherited_region = None

    def _semantic_collect_applicable_styles(self, dataset, style_type):
        referenced_styles = []
        inherited_styles = []
        region_styles = []
        if self.style is not None:
            # Styles cascade
            for style_id in self.style:
                try:
                    style = dataset['tt_element'].get_element_by_id(elem_id=style_id, elem_type=style_type)
                    for style_binding in style.ordered_styles(dataset=dataset):
                        if style_binding not in referenced_styles:
                            referenced_styles.append(style_binding)
                except LookupError:
                    raise SemanticValidationError(ERR_SEMANTIC_STYLE_MISSING.format(style=style_id))

            # Push this validated set onto the stack for children to use

        for style_list in dataset['styles_stack']:
            # Traverse all the styles encountered at our parent elements
            for inh_style in style_list:
                if inh_style not in referenced_styles and inh_style not in inherited_styles:
                    inherited_styles.append(inh_style)

        region = dataset.get('region', None)
        self._inherited_region = region

        if region is not None:
            # At last apply any region styles we may find
            for region_style in region.validated_styles:
                if region_style not in referenced_styles and region_style not in inherited_styles:
                    region_styles.append(region_style)

        self._referenced_styles = referenced_styles
        self._validated_styles = referenced_styles + inherited_styles + region_styles

    def _semantic_push_styles(self, dataset):
        dataset['styles_stack'].append(self._referenced_styles)

    def _semantic_pop_styles(self, dataset):
        dataset['styles_stack'].pop()

    def effective_style(self):
        """
        In particular because of fontSize cascading semantics we need to be able to calculate the effective fontSize
        in any styled element container. Without it conversion from absolute values to relative would not be possible.
        :return:
        """
        return self._compatible_style_type.calculate_effective_style

    @property
    def validated_styles(self):
        if self._validated_styles is None:
            raise SemanticValidationError(ERR_SEMANTIC_VALIDATION_EXPECTED)
        return self._validated_styles

    @property
    def inherited_region(self):
        return self._inherited_region


class RegionedElementMixin(object):
    """
    Makes sure we always know where we are. Detects double region assignment which is a warning.
    """

    def _semantic_set_region(self, dataset, region_type):
        if self.region is not None:
            try:
                region = dataset['tt_element'].get_element_by_id(self.region, region_type)
                dataset['region'] = region
            except LookupError:
                raise SemanticValidationError(ERR_SEMANTIC_REGION_MISSING.format(
                    region=self.region
                ))

    def _semantic_unset_region(self, dataset):
        if self.region is not None:
            dataset['region'] = None