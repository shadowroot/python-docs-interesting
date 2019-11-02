import random
import hashlib
import codecs
import time
import functools
import json
import string

class DataFuzzer():

    NOT_EXPANDABLE_TYPES = set("bytes", "str", "int", "float")
    EXPANDABLE_TYPES = set("dict", "list", "set")
    MAX_SIZE = 4*1024*1024*1024
    MAX_ELEMENTS_ON_LEVEL = 100
    AVOID_TYPES = []
    CALC_TIMEOUT = 100

    def __init__(self, **kwargs):
        self._current_level = 0
        self._current_size = 0
        self._min_levels = 0
        self._type = None
        self._size = 0
        self._depth = 0

        if kwargs is not None:
            self.__dict__.update(kwargs)
        else:
            raise ValueError("No configuration was provided")

    def _validate_conf(self):
        if self._type not in set(self.EXPANDABLE_TYPES, self.NOT_EXPANDABLE_TYPES):
            raise ValueError("Invalid type")
        if self._type == "dict" and (not hasattr(self, "_depth") or self._depth > 200):
            raise ValueError("Invalid depth for dict")
        if self._size > self.MAX_SIZE:
            raise ValueError("This script is not suitable for this kind of size of input data.")

    def _get_types_set(self):
        types = self.NOT_EXPANDABLE_TYPES
        if self._current_level < self._depth:
            types.update(self.EXPANDABLE_TYPES)

        types_choice_set = [_t for _t in types if _t not in self.AVOID_TYPES]
        return types_choice_set

    def _is_oversized(self):
        if self._current_size >= self._size:
            return False
        return True

    def _generator_for_complex(self, elements_on_level, types_choice_set):
        generated_value = None
        bytes_generated_value = None
        for _ in range(elements_on_level):
            t = random.choice(types_choice_set)
            generator = getattr(self, "_generate_{}".format(t))
            t_start = time.time()
            while not ok:
                if (time.time() - t_start) > self.CALC_TIMEOUT:
                    raise TimeoutError("Time for generating expired")
                generated_value = generator()
                bytes_generated_value = bytes(json.dumps(generated_value))
                if (len(bytes_generated_value) + self._current_size + elements_on_level + self._depth - self._current_level) <= self._size:
                    ok = True
        return generated_value, bytes_generated_value

    def _generate_dict(self):
        """Universal struct for now"""
        result = {}
        if self._is_oversized():
            return result
        types_choice_set = self._get_types_set()
        elements_on_level = random.randint(1, self.MAX_ELEMENTS_ON_LEVEL)
        generated_value, bytes_generated_value = self._generator_for_complex(elements_on_level, types_choice_set)
        result[hashlib.sha256(bytes_generated_value)] = generated_value
        self._current_size += len(bytes_generated_value)
        self._current_level += 1 

        return result
        
    def _generate_list(self):
        result = []
        if self._is_oversized():
            return result
        types_choice_set = self._get_types_set()
        elements_on_level = random.randint(1, self.MAX_ELEMENTS_ON_LEVEL)
        generated_value, bytes_generated_value = self._generator_for_complex(elements_on_level, types_choice_set)
        result.append(generated_value)
        self._current_size += len(bytes_generated_value)
        self._current_level += 1 
    
    def _generate_set(self):
        result = set()
        if self._is_oversized():
            return result
        types_choice_set = self._get_types_set()
        elements_on_level = random.randint(1, self.MAX_ELEMENTS_ON_LEVEL)
        generated_value, bytes_generated_value = self._generator_for_complex(elements_on_level, types_choice_set)
        result.update(generated_value)
        self._current_size += len(bytes_generated_value)
        self._current_level += 1 
        
    def _generate_bytes(self):
        if self._is_oversized():
            return bytes()
        return bytes(bytearray(random.getrandbits(8) for _ in range(self._size - self._current_size)))
    
    def _generate_str(self):
        if self._is_oversized():
            return ""
        return "".join([random.choice(string.ascii_letters) for _ in range(self._size - self._current_size)])
    
    def _generate_int(self):
        if self._is_oversized():
            return int()
        return random.randint(0, 1000)

    def _generate_float(self):
        if self._is_oversized():
            return float()
        return float(random.random())
    
