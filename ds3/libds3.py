#   Copyright 2014-2015 Spectra Logic Corporation. All Rights Reserved.
#   Licensed under the Apache License, Version 2.0 (the "License"). You may not use
#   this file except in compliance with the License. A copy of the License is located at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   or in the "license" file accompanying this file.
#   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied. See the License for the
#   specific language governing permissions and limitations under the License.

from ctypes import *
import platform

lib = None

if platform.system() == "Darwin":
    lib = cdll.LoadLibrary("libds3.dylib")
else:
    lib = cdll.LoadLibrary("libds3.so")

def asCList(orig):
    cList = (ctypes.c_char_p * len(orig))()
    cList[:] = orig
    return cList

def toDs3BulkObjectList(fileList):
    bulkList = lib.ds3_init_bulk_object_list(len(fileList))
    bulkContents = bulkList.contents.list
    for i in xrange(len(fileList)):
        if isinstance(fileList[i], tuple):
            bulkContents[i].name = lib.ds3_str_init(fileList[i][0])
            bulkContents[i].length = fileList[i][1]
        else:
            bulkContents[i].name = lib.ds3_str_init(fileList[i])
    return bulkList

class LibDs3Str(Structure):
    _fields_ = [("value", c_char_p), ("size", c_size_t)]

class LibDs3Creds(Structure):
    _fields_ = [("access_id", POINTER(LibDs3Str)), ("secret_key", POINTER(LibDs3Str))]

class LibDs3Client(Structure):
    _fields_ = [("endpoint", POINTER(LibDs3Str)), ("proxy", POINTER(LibDs3Str)), ("num_redirects", c_ulonglong), ("creds", POINTER(LibDs3Creds))]

class LibDs3ErrorResponse(Structure):
    _fields_ = [("status_code", c_ulonglong), ("status_message", POINTER(LibDs3Str)), ("error_body", POINTER(LibDs3Str))]

class LibDs3ErrorCode(object):
    DS3_ERROR_INVALID_XML = 0
    DS3_ERROR_CURL_HANDLER = 1
    DS3_ERROR_REQUEST_FAILED = 2
    DS3_ERROR_MISSING_ARGS = 3
    DS3_ERROR_BAD_STATUS_CODE = 4

class LibDs3Error(Structure):
    _fields_ = [("ds3_error_code", c_int), ("message", POINTER(LibDs3Str)), ("error", POINTER(LibDs3ErrorResponse))]

class LibDs3Bucket(Structure):
    _fields_ = [("creation_date", POINTER(LibDs3Str)), ("name", POINTER(LibDs3Str))]

class LibDs3Owner(Structure):
    _fields_ = [("name", POINTER(LibDs3Str)), ("id", POINTER(LibDs3Str))]

class LibDs3Object(Structure):
    _fields_ = [("name", POINTER(LibDs3Str)), ("etag", POINTER(LibDs3Str)), ("size", c_ulonglong), ("owner", POINTER(LibDs3Owner)), ("last_modified", POINTER(LibDs3Str)), ("storage_class", POINTER(LibDs3Str))]

class LibDs3SearchObject(Structure):
    _fields_ = [("bucket_id", POINTER(LibDs3Str)), ("id", POINTER(LibDs3Str)), ("name", POINTER(LibDs3Str)), ("size", c_ulonglong), ("owner", POINTER(LibDs3Owner)), ("last_modified", POINTER(LibDs3Str)), ("storage_class", POINTER(LibDs3Str)), ("type", POINTER(LibDs3Str)), ("version", POINTER(LibDs3Str))]

class LibDs3GetServiceResponse(Structure):
    _fields_ = [("buckets", POINTER(LibDs3Bucket)), ("num_buckets", c_size_t), ("owner", POINTER(LibDs3Owner))]

class LibDs3GetBucketResponse(Structure):
    _fields_ = [("objects", POINTER(LibDs3Object)), ("num_objects", c_size_t), ("creation_date", POINTER(LibDs3Str)), ("is_truncated", c_bool), ("marker", POINTER(LibDs3Str)), ("delimiter", POINTER(LibDs3Str)), ("max_keys", c_int), ("name", POINTER(LibDs3Str)), ("next_marker", POINTER(LibDs3Str)), ("prefix", POINTER(LibDs3Str)), ("common_prefixes", POINTER(POINTER(LibDs3Str))), ("num_common_prefixes", c_ulonglong)]

class LibDs3GetObjectsResponse(Structure):
    _fields_ = [("objects", POINTER(POINTER(LibDs3SearchObject))), ("num_objects", c_ulonglong)]

class LibDs3BulkObject(Structure):
    _fields_ = [("name", POINTER(LibDs3Str)), ("length", c_ulonglong), ("offset", c_ulonglong), ("in_cache", c_bool)]

class LibDs3BulkObjectList(Structure):
    _fields_ = [("list", POINTER(LibDs3BulkObject)), ("size", c_ulonglong), ("chunk_number", c_ulonglong), ("node_id", POINTER(LibDs3Str)), ("server_id", POINTER(LibDs3Str)), ("chunk_id", POINTER(LibDs3Str))]

class LibDs3ChunkOrdering(object):
    IN_ORDER = 0
    NONE = 1

class LibDs3Priority(object):
    CRITIAL = 0
    VERY_HIGH = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5
    MINIMIZED_DUE_TO_TOO_MANY_REQUESTS = 6
class LibDs3RequestType(object):
    PUT = 0
    GET = 1

class LibDs3WriteOptimization(object):
    CAPACITY = 0
    PERFORMANCE = 1

class LibDs3JobStatus(object):
    IN_PROGRESS = 0
    COMPLETED = 1
    CANCELED = 2

class LibDs3BulkResponse(Structure):
    _fields_ = [("bucket_name", POINTER(LibDs3Str)), ("cached_size_in_bytes", c_ulonglong), ("chunk_ordering", c_int), ("completed_size_in_bytes", c_ulonglong), ("job_id", POINTER(LibDs3Str)), ("original_size_in_bytes", c_ulonglong), ("ds3_job_priority", c_int), ("request_type", c_int), ("start_date", POINTER(LibDs3Str)), ("user_id", POINTER(LibDs3Str)), ("user_name", POINTER(LibDs3Str)), ("write_optimization", c_int), ("list", POINTER(POINTER(LibDs3BulkObjectList))), ("list_size", c_size_t), ("status", c_int)]

class LibDs3GetJobsResponse(Structure):
    _fields_ = [("jobs", POINTER(POINTER(LibDs3BulkResponse))), ("jobs_size", c_size_t)]

class LibDs3Tape(Structure):
    _fields_ = [("barcode", POINTER(LibDs3Str))]

class LibDs3GetPhysicalPlacementResponse(Structure):
    _fields_ = [("tapes", POINTER(LibDs3Tape)), ("num_tapes", c_ulonglong)]

class LibDs3AllocateChunkResponse(Structure):
    _fields_ = [("objects", POINTER(LibDs3BulkObjectList)), ("retry_after", c_ulonglong)]

class LibDs3GetAvailableChunksResponse(Structure):
    _fields_ = [("object_list", POINTER(LibDs3BulkResponse)), ("retry_after", c_ulonglong)]

class LibDs3BuildInformation(Structure):
    _fields_ = [("branch", POINTER(LibDs3Str)), ("revision", POINTER(LibDs3Str)), ("version", POINTER(LibDs3Str))]

class LibDs3GetSystemInformationResponse(Structure):
    _fields_ = [("api_version", POINTER(LibDs3Str)), ("serial_number", POINTER(LibDs3Str)), ("build_information", POINTER(LibDs3BuildInformation))]

class LibDs3VerifySystemHealthResponse(Structure):
    _fields_ = [("ms_required_to_verify_data_planner_health", c_ulonglong)]

class LibDs3Request(Structure):
    pass

class LibDs3Metadata(Structure):
    pass

class LibDs3MetadataKeysResult(Structure):
    _fields_ = [("keys", POINTER(POINTER(LibDs3Str))), ("num_keys", c_ulonglong)]

class LibDs3MetadataGetEntryResult(Structure):
    _fields_ = [("name", POINTER(LibDs3Str)), ("values", POINTER(POINTER(LibDs3Str))), ("num_values", c_ulonglong)]

lib.ds3_str_init.restype = POINTER(LibDs3Str)

lib.ds3_metadata_keys.restype = POINTER(LibDs3MetadataKeysResult)
lib.ds3_metadata_get_entry.restype = POINTER(LibDs3MetadataGetEntryResult)

lib.ds3_create_creds.restype = POINTER(LibDs3Creds)
lib.ds3_create_client.restype = POINTER(LibDs3Client)
lib.ds3_create_client_from_env.restype = POINTER(LibDs3Error)
lib.ds3_create_client_from_env.restype = POINTER(LibDs3Error)
lib.ds3_init_get_jobs.restype = POINTER(LibDs3Request)
lib.ds3_init_get_system_information.restype = POINTER(LibDs3Request)
lib.ds3_init_verify_system_health.restype = POINTER(LibDs3Request)
lib.ds3_init_get_service.restype = POINTER(LibDs3Request)
lib.ds3_init_get_bucket.restype = POINTER(LibDs3Request)
lib.ds3_init_delete_folder.restype = POINTER(LibDs3Request)
lib.ds3_init_get_object_for_job.restype = POINTER(LibDs3Request)
lib.ds3_init_put_bucket.restype = POINTER(LibDs3Request)
lib.ds3_init_put_object_for_job.restype = POINTER(LibDs3Request)
lib.ds3_init_delete_bucket.restype = POINTER(LibDs3Request)
lib.ds3_init_delete_object.restype = POINTER(LibDs3Request)
lib.ds3_init_delete_objects.restype = POINTER(LibDs3Request)
lib.ds3_init_head_object.restype = POINTER(LibDs3Request)
lib.ds3_init_head_bucket.restype = POINTER(LibDs3Request)
lib.ds3_init_allocate_chunk.restype = POINTER(LibDs3Request)
lib.ds3_init_get_available_chunks.restype = POINTER(LibDs3Request)
lib.ds3_init_put_bulk.restype = POINTER(LibDs3Request)
lib.ds3_init_get_bulk.restype = POINTER(LibDs3Request)
lib.ds3_init_get_objects.restype = POINTER(LibDs3Request)
lib.ds3_init_get_physical_placement.restype = POINTER(LibDs3Request)
lib.ds3_init_get_physical_placement_full_details.restype = POINTER(LibDs3Request)
lib.ds3_init_get_job.restype = POINTER(LibDs3Request)
lib.ds3_init_put_job.restype = POINTER(LibDs3Request)
lib.ds3_init_delete_job.restype = POINTER(LibDs3Request)
lib.ds3_get_jobs.restype = POINTER(LibDs3Error)
lib.ds3_get_system_information.restype = POINTER(LibDs3Error)
lib.ds3_verify_system_health.restype = POINTER(LibDs3Error)
lib.ds3_get_service.restype = POINTER(LibDs3Error)
lib.ds3_get_bucket.restype = POINTER(LibDs3Error)
lib.ds3_get_object.restype = POINTER(LibDs3Error)
lib.ds3_get_objects.restype = POINTER(LibDs3Error)
lib.ds3_delete_folder.restype = POINTER(LibDs3Error)
lib.ds3_bulk.restype = POINTER(LibDs3Error)
lib.ds3_allocate_chunk.restype = POINTER(LibDs3Error)
lib.ds3_get_available_chunks.restype = POINTER(LibDs3Error)
lib.ds3_delete_bucket.restype = POINTER(LibDs3Error)
lib.ds3_delete_object.restype = POINTER(LibDs3Error)
lib.ds3_head_object.restype = POINTER(LibDs3Error)
lib.ds3_head_bucket.restype = POINTER(LibDs3Error)
lib.ds3_delete_objects.restype = POINTER(LibDs3Error)
lib.ds3_put_bucket.restype = POINTER(LibDs3Error)
lib.ds3_put_object.restype = POINTER(LibDs3Error)
lib.ds3_get_job.restype = POINTER(LibDs3Error)
lib.ds3_put_job.restype = POINTER(LibDs3Error)
lib.ds3_delete_job.restype = POINTER(LibDs3Error)
lib.ds3_get_objects.restype = POINTER(LibDs3Error)
lib.ds3_get_physical_placement.restype = POINTER(LibDs3Error)

lib.ds3_write_to_file.restype = c_size_t
lib.ds3_read_from_file.restype = c_size_t
lib.ds3_write_to_fd.restype = c_size_t
lib.ds3_read_from_fd.restype = c_size_t

lib.ds3_init_bulk_object_list.restype = POINTER(LibDs3BulkObjectList)
lib.ds3_convert_file_list.restype = POINTER(LibDs3BulkObjectList)
