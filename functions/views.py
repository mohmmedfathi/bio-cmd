from django.http import HttpResponse
from django.shortcuts import redirect, render
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from Bio import SeqIO
from Bio import AlignIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import sys, getopt
from django.core.files import File

from django.core.files.uploadedfile import UploadedFile


def index(request):
    return render(request,'home.html')


def home(request):
    return render(request,'index.html')


def gc_precentage(request):
    return render(request,'gcprecentage.html')

def resultgc_precentage(request):
    if request.method == 'POST':
        DNA = request.POST["num1"]
        for i in DNA:
            if i not in 'AGCTN':
                return render(request,'resultgcprecentage.html',{"p":'Invalid Seq'})
        DNA = DNA.upper()
        nBases = DNA.count('N')
        gcBases = DNA.count('G') + DNA.count('C')
        precantage = (gcBases / (len(DNA) - nBases)) * 100
        return render(request,'resultgcprecentage.html',{"p":precantage})
    else:
        return redirect("/")


def complement(DNA):
    DNA = DNA.upper()
    baseComplement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}
    letters = list(DNA)
    letters = [baseComplement[base] for base in letters]
    return ''.join(letters)

def reverse(DNA):
    return DNA[::-1]

def reverse_complement(request):
    return render(request,'reversecomplement.html')

def ResultReverse_complement(request):
    if request.method == 'POST':
        DNA = request.POST["num1"]
        for i in DNA:
            if i not in 'AGCT':
                return render(request,'Resultreversecomplement.html',{"p":'Invalid Seq'})
        seq = complement(DNA)
        seq = reverse(seq)
        return render(request,'Resultreversecomplement.html',{"p":seq})
    else:
        return redirect("/")

def transcribe(request):
    return render(request,'transcribe.html')

def Resulttranscribe(request):
    if request.method == 'POST':
        DNA = request.POST["num1"]
        DNA = DNA.upper()
        for i in DNA:
            if i not in 'AGCT':
                return render(request,'Resulttranscribe.html',{"p":'Invalid Seq'})
        return render(request,'Resulttranscribe.html',{"p":DNA.replace('T', 'U')})
    else:
        return redirect("/")


def calc_nbases(request):
    return render(request,'calc_nbases.html')

def resultcalc_nbases(request):
    if request.method == 'POST':
        DNA = request.POST["num1"]
        DNA = DNA.upper()
        for i in DNA:
            if i not in 'AGCTN':
                return render(request,'resultcalc_nbases.html',{"p":'Invalid Seq'})

        return render(request,'resultcalc_nbases.html',{"p":DNA.count('N')})
    else:
        return redirect("/")

def check_Protein(protein):
    protein = protein.upper()
    for i in protein:
        if i not in 'ABCDEFGHIKLMNPQRSTVWXYZ':
            return False
    return True

def check_DNA(DNA):
    DNA = DNA.upper()
    for i in DNA:
        if i not in 'AGCT':
            return False
    return True

def check_RNA(RNA):
    RNA = RNA.upper()
    for i in RNA:
        if i not in 'AGCU':
            return False
    return True


def is_valid(request):
    return render(request,'isvalid.html')
def resultis_valid(request):
    if request.method == 'POST':
        Seq = request.POST["num1"]
        type = request.POST["num2"]
        type = type.lower()
        if type == 'protein':
            if check_Protein(Seq):
                return render(request,'resultcheck_DNA.html',{"p": "it's a valid protein"})
            else:
                return render(request,'resultcheck_DNA.html',{"p": "it's not valid protein"})
        elif type == 'dna':
            if check_DNA(Seq):
                return render(request,'resultcheck_DNA.html',{"p": "it's a valid Dna"})
            else:
                return render(request,'resultcheck_DNA.html',{"p": "it's not valid Dna"})
        elif type == 'rna':
            if check_RNA(Seq):
                return render(request,'resultcheck_DNA.html',{"p": "it's a valid Rna"})
            else:
                return render(request,'resultcheck_DNA.html',{"p": "it's not valid Rna"})
        else:
            return render(request,'resultcheck_DNA.html',{"p": 'Invalid Type or invalid Sequance'})

    else:
        return redirect("/")


def filter_nbases(request):
    return render(request,'filter_nbases.html')
def Resultfilter_nbases(request):
    """This command takes a seq and returns the Seq after removing n bases."""
    if request.method == 'POST':
        Seq = request.POST["num1"]
        Seq = Seq.upper()
        for i in Seq:
            if i not in 'AGCTN':
                return render(request,'Resultfilter_nbases.html',{"p":'Invalid Seq'})
        Seq = Seq.replace("N", "")
        return render(request,'Resultfilter_nbases.html',{"p":Seq})
    else:
        return redirect("/")


def output_alignment(alignments, output):
    f = open(output, 'w')
    for alignment in alignments:
        nonFormattedAlignment = str(alignment)
        f.write(nonFormattedAlignment)
        f.write('\n')
        formattedAlignment = str(format_alignment(*alignment))
        f.write(formattedAlignment)
        f.write('\n')
    f.close()

def seq_alignment(request):
    return render(request,'seq_alignment.html')
def rseqalignment(request):
    if request.method == 'POST':
        output = request.POST["file"]
        seq1 = request.POST["seq1"]
        seq2 = request.POST["seq2"]
        for i in seq1:
            if i not in 'AGCT':
                return render(request,'Rseq_alignment.html',{"p":'Seq1 Invalid'})
        for j in seq2:
            if j not in 'AGCT':
                return render(request,'Rseq_alignment.html',{"p":'Seq2 Invalid'})
        alignments = pairwise2.align.globalxx(seq1, seq2)
        if output == '':
            alig = []
            for alignment in alignments:
                alig.append(alignment)
                alig.append(format_alignment(*alignment))
                
            return render(request,'Rseq_alignment.html',{"alignment":alig})
        else:
            output_alignment(alignments, output)
            s = 'Alignmnet Done to File ' + output 
            return render(request,'Rseq_alignment.html',{"p":s})
    else:
        return redirect("/")


def seq_alignment_files(request):
    return render(request,'seq_alignment_files.html')
def rseq_alignment_files(request):
    if request.method == 'POST':
        outputfile = request.POST["file"]
        file1 = request.POST["seq1"]
        file2 = request.POST["seq2"]
        try:
            seq1 = SeqIO.read(file1, 'fasta')
            seq2 = SeqIO.read(file2, 'fasta')
        except OSError as Error:
            return render(request,'rseq_alignment_files.html',{"alignment":'Please Enter a valid File name'})
        alignments = pairwise2.align.globalxx(seq1, seq2)
        if outputfile == '':
            alig = []
            for alignment in alignments:
                alig.append(alignment)
                alig.append(format_alignment(*alignment))
            return render(request,'rseq_alignment_files.html',{"ali":alig})
        else:
            output_alignment(alignments, outputfile)
            s = 'Alignmnet Done to File ' + outputfile 
            return render(request,'rseq_alignment_files.html',{"alignment":s})
    else:
        return redirect("/")



def merge_fasta(request):
    return render(request,'merge_fasta.html')
def rmerge_fasta(request):
    if request.method == 'POST':
        file1 = request.POST["seq1"]
        file2 = request.POST["seq2"]
        output = request.POST["file"]
        try:
            file1 = SeqIO.parse(file1, 'fasta')
            file2 = SeqIO.parse(file2, 'fasta')
        except OSError as Error:
            return render(request,'rmerge_fasta.html',{"fi":Error})

        FilesList = []
        FilesList.append(file1)
        FilesList.append(file2)
        if output == '':
            fi = []
            for file in FilesList:
                for record in file:
                    fi.append(record.id)
                    fi.append(record.description)
                    fi.append(record.seq)
                fi.append("\n")
            return render(request,'rmerge_fasta.html',{"po":fi})
        else:
            with open(output, 'w')as outputFile:
                for file in FilesList:
                    SeqIO.write(file, outputFile, 'fasta')
            f1 = "The sequence done in output file " + output
            return render(request,'rmerge_fasta.html',{"fi":f1})
    else:
        return redirect("/")


def convert_to_fasta(request):
    return render(request,'convert_to_fasta.html')
def Rconvert_to_fasta(request):
    if request.method == 'POST':
        file = request.POST["file"]
        if file[-3:] == 'gbk':
            output = file[:-3] + 'fasta'
            try:
                with open(file)as input:
                    sequance = SeqIO.parse(input, 'genbank')
                    SeqIO.write(sequance, output, 'fasta')
                    s = 'Conversion Done to ' + output                
                    return render(request,'Rconvert_to_fasta.html',{"s":s})
            except OSError as Error:
                return render(request,'Rconvert_to_fasta.html',{"s":Error})

        else:
            s = 'File must be genbank\n'
            return render(request,'Rconvert_to_fasta.html',{"s":s})
    else:
        return redirect("/")

def MA(request):
    return render(request,'MA.html')
def RMA(request):
    if request.method == 'POST':
        file = request.POST["file"]
        alignment = AlignIO.read(file,"stockholm")
        lst = []
        lst.append(alignment)
        lst.append("\n")
        lst.append("Showing Alignment Sequence Record")
        for align in alignment:
            lst.append(align.seq)
        lst.append("\n")
        AlignIO.read(open(file), "stockholm")
        lst.append(format(alignment, "fasta"))
        return render(request,'RMA.html',{"lst":lst})

    else:
        return redirect("/")