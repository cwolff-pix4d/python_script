#import Pix4Dmatic
import os
import shutil
from datetime import datetime
import platform
import numpy as np




project_path = r"C:\Users\cwolff\Documents\Pix4Dmatic\log\root.p4a"
app = session()
project = app.open_project(project_path)

cluster = project.active_cluster
print("bla")
#status = cluster.reconstruct()
#print(f'Reconstruction status : {cluster.reconstruction.status}')

#status.wait()

#print(f'Reconstruction status : {cluster.reconstruction.status}')

metrics = cluster.reconstruction.metrics
"""print(help(metrics))
print(help(metrics.gcps.gcp))
print(help(metrics.atps))
print("1")
print((metrics.gcps.position_error_sigmas))
print((metrics.gcps.position_error_RMSs))
print((metrics.gcps.position_error_means))
print(help(metrics.gcps))"""
for key, value in metrics.gcps.gcp.items():
    print(metrics.gcps.gcp[key].position_error)
    print(value.position_error)
    print(str(metrics.gcps.gcp[key].mean_reprojection_error))
    print(str(metrics.gcps.gcp[key].number_valid_reprojections))
    print(str(metrics.gcps.gcp[key].number_user_image_marks))
    print(key)
print("2")
cluster.export_gcp_metrics(r"C:\Users\cwolff\Desktop\QA_bMERGE\metrics.txt")
cluster.export_gcp_metrics(r"C:\Users\cwolff\Desktop\QA_bMERGE\metrics.csv")








"""
void bindGcpMetrics(pybind11::module& module)
{
    pybind11::class_<GcpMetrics>(module, "GcpMetrics")
        .def_property_readonly("position_error_means", [](const GcpMetrics& self) { return self.positionErrorMeans; })
        .def_property_readonly("position_error_sigmas", [](const GcpMetrics& self) { return self.positionErrorSigmas; })
        .def_property_readonly("position_error_RMSs", [](const GcpMetrics& self) { return self.positionErrorRmss; })
        .def("position_error",
             [](const GcpMetrics& self, QString gcpName) {
                 if (self.gcpErrors.find(gcpName) == self.gcpErrors.end())
                     throw pybind11::index_error();
                 const auto& e = self.gcpErrors.at(gcpName).positionError;
                 return pybind11::make_tuple(e.x, e.y, e.z);
             })
        .def("mean_reprojection_error",
             [](const GcpMetrics& self, QString gcpName) {
                 if (self.gcpErrors.find(gcpName) == self.gcpErrors.end())
                     throw pybind11::index_error();
                 return self.gcpErrors.at(gcpName).meanReprojectionError;
             })
        .def("number_valid_reprojections",
             [](const GcpMetrics& self, QString gcpName) {
                 if (self.gcpErrors.find(gcpName) == self.gcpErrors.end())
                     throw pybind11::index_error();
                 return self.gcpErrors.at(gcpName).validReprojectionCount;
             })
        .def("number_user_image_marks",
             [](const GcpMetrics& self, QString gcpName) {
                 if (self.gcpErrors.find(gcpName) == self.gcpErrors.end())
                     throw pybind11::index_error();
                 return self.gcpErrors.at(gcpName).userImageMarkCount;
             })
        .def("__repr__", [](const ReconstructionMetrics&) { return "GcpMetrics"; });
}
ProcessingStatus ClusterWrapper::exportGcpMetrics(const std::string& filePath)
{
    ClusterExecutor executor(*m_cluster);
    return {m_cluster,
            executor.post(m_parentProject->context(), exportGcpMetricsToCsv(extensions::appendIfMissing(
                                                          QString::fromStdString(filePath), extensions::txt)))};
"""