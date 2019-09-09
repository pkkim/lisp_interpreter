(def nil (list))

'(This somehow feels bad)
(def eval (lambda (x) (eval x)))
(def quote (lambda (x) (quote x)))

(def filter
	 (lambda (f l)
	   (if (= l nil)
		 nil
		 (if (f (car l))
		   (cons (car l) (filter f (cdr l)))
		   (filter f (cdr l))))))

(def map
	 (lambda (f l)
	   (if (= l nil)
		 nil
		 (cons (f (car l)) (map f (cdr l))))))

(def reduce
	 (lambda (f l init)
	   (if (= l nil)
		 init
		 (reduce f (cdr l) (f init (car l))))))
