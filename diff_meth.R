library(methylKit)
file.list1 <- list.files("Control", pattern = "*.methylKit", full.names = T)
file.list2 <- list.files("Case", pattern = "*.methylKit", full.names = T)

f.list = c(file.list1,file.list2)

file.list <- lapply(f.list, function(x) list(x)[[1]])
control_samples = n1
case_samples = n2
myobj=methRead(file.list,
               sample.id=as.list(c(paste0("control",1:n1), paste0("case",1:n2))),
               assembly="BosVos",
               treatment=c(rep(0, times=n1),rep(1, times=n2)),
               context="CpG",
               mincov = 5,
               dbdir="MethylKit"
)


filtered.myobj=filterByCoverage(myobj,lo.count=5,lo.perc=NULL,
                                hi.count=NULL,hi.perc=99.9)
                                
meth=unite(myobj, destrand=T)
myDiff=calculateDiffMeth(meth)
all.diff=getMethylDiff(myDiff, difference=25,qvalue=0.01, type="all")
write.csv(all.diff, file="diff_meth_treat_25.csv")
