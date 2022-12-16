from . import views
from django.urls import path


urlpatterns = [

    path('',views.index,name="home"),
    path('home',views.home,name="homee"),

    path('gcprecentage',views.gc_precentage,name="gcprecentage"),
    path('resultgcprecentage',views.resultgc_precentage,name="resultgcprecentage"),

    path('reversecomplement',views.reverse_complement,name="gcprecentage"),
    path('resultreversecomplement',views.ResultReverse_complement,name="resultgcprecentage"),

    path('transcribe',views.transcribe , name="transcribe"),
    path('resulttranscribe',views.Resulttranscribe,name="resulttranscribe"),

    path('calcnbases',views.calc_nbases , name="calcnbases"),
    path('resultcalcnbases',views.resultcalc_nbases,name="resultcalcnbases"),

    path('isvalid',views.is_valid , name="resultis_valid"),
    path('resultisvalid',views.resultis_valid,name="resultis_valid"),

    path('filternbases',views.filter_nbases,name="filternbases"),
    path('resultfilternbases',views.Resultfilter_nbases,name="resultfilternbases"),

    path('seqalignment',views.seq_alignment,name="seqalignment"),
    path('rseqalignment',views.rseqalignment,name="rseqalignment"),

    path('seqalignmentfiles',views.seq_alignment_files,name="seqalignmentfiles"),
    path('rseqalignmentfiles',views.rseq_alignment_files,name="rseqalignmentfiles"),

    path('mergefasta',views.merge_fasta,name="mergefasta"),
    path('rmergefasta',views.rmerge_fasta,name="rmergefasta"),

    path('converttofasta',views.convert_to_fasta,name="converttofasta"),
    path('rconverttofasta',views.Rconvert_to_fasta,name="rconverttofasta"),

    path('ma',views.MA,name="ma"),
    path('rma',views.RMA,name="rma"),

]
