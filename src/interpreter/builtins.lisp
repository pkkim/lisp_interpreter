(def filter
	 (lambda (f l)
	   (if (= l '())
		 '()
		 (if (f (car l))
		   (cons (car l) (filter f (cdr l)))
		   (filter f (cdr l))))))

(def map
	 (lambda (f l)
	   (if (= l '())
		 '()
		 (cons (f (car l)) (map f (cdr l))))))
